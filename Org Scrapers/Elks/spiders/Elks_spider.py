import scrapy
import json

class ElksSpider(scrapy.Spider):
	name = "elks"
	base_url = "https://www.elks.org/lodges/default.cfm"
	domain = "https://www.elks.org"

	def __init__(self):
		self.results = []

	def start_requests(self):
		yield scrapy.Request(url=self.base_url, callback=self.parse)

	def parse(self, response):
		states = response.xpath("//select[@id='State']//option/@value").extract()
		for state in states[1:]:
			yield scrapy.FormRequest(url=self.base_url,
				formdata={
					"LodgeName": "",
					"LodgeZipCode": "",
					"State": state,
					"District": "",
					"SortBy": "LodgeName",
					"STARTROW": "1"
				},
				callback=self.parse_list)

	def parse_list(self, response):
		lodges = response.xpath("//div[@class='innercolumn']//li//a")
		for lodge in lodges:
			name = self.validate(lodge.xpath("./text()"))
			url = self.validate(lodge.xpath("./@href"))

			yield scrapy.Request(url=self.domain+url, 
				meta={'name': name}, callback=self.parse_detail)

	def parse_detail(self, response):
		item = dict()
		item['lodge_name'] = response.meta['name']
		item['lodge_number'] = response.url.split("LodgeNumber=")[-1].strip()

		contacts = response.xpath("//ul[@class='plain roster gray']//li")
		item['contact'] = ""
		for contact in contacts:
			title = self.validate(contact.xpath(".//strong/text()"))
			if title == "Secretary:":
				item['contact'] = [tp.strip() 
					for tp in contact.xpath("./text()").extract()
					if tp.strip()!=""][0]

		addresses = response.xpath("//div[@style='clear: both;']")
		item['address'] = ""
		item['phone'] = ""
		item['email'] = ""
		item['website'] = ""
		for address in addresses:
			title = self.validate(address.xpath(".//h3/text()"))
			if title == 'Lodge Location':
				value = [tp.strip() for tp in address.xpath(".//p/text()").extract() if tp.strip()!=""]
				if len(value) == 1:
					item['address'] = value[0]
				else:
					item['address'] = ", ".join(value[-2:])

			if title == "Lodge Contact Information":
				phones = address.xpath(".//li")
				for phone in phones:
					temp = self.validate(phone.xpath(".//strong/text()"))
					if temp == "Telephone:":
						item['phone'] = [tp.strip() 
								for tp in phone.xpath("./text()").extract()
								if tp.strip()!=""][0].split(" ")[0]

					if temp == "E-mail:":
						item['email'] = self.validate(phone.xpath(".//a/text()"))

					if temp == "Website:":
						item['website'] = self.validate(phone.xpath(".//a/text()"))

		self.results.append(item)
		print json.dumps(item, indent=4)

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""