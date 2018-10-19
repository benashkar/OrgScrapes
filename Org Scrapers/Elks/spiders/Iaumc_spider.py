import scrapy
import json
import re

class IaumcSpider(scrapy.Spider):
	name = "iaumc"
	base_url = "https://www.iaumc.org/churches"
	domain = "https://www.iaumc.org"

	def __init__(self):
		self.results = []

	def start_requests(self):
		yield scrapy.Request(url=self.base_url, callback=self.parse)

	def parse(self, response):
		churches = response.xpath("//div[@class='col-sm-9']/div//a")

		for church in churches:
			title = self.validate(church.xpath("./text()"))
			url = self.validate(church.xpath("./@href"))
			yield scrapy.Request(url=self.domain+url, 
				meta={'title': title},
				callback=self.parse_detail)
			# break

	def parse_detail(self, response):
		item = dict()
		item['org_name'] = response.meta['title'].replace(",", "").strip() + " United Methodist Church"
		match = re.search(r'[\w\.-]+@[\w\.-]+', response.body)
		item['email'] = match.group(0)
		try:
			item['phone'] = re.findall(r'\d{3}-\d{3}-\d{4}', response.body)[0]
		except:
			item['phone'] = 0

		if "Driving Directions" not in response.body:
			split_token = "<h3>"
		else:
			split_token = "Driving Directions"
 		try:
			token = self.cleanhtml(response.body.split('Physical address')[1].split(split_token)[0].strip())
		except:
			token = self.cleanhtml(response.body.split('Mailing Address')[1].split(split_token)[0].strip())
		address = [" ".join(tp.strip().split()).replace(",", "").strip() for tp in token.split("\n") if tp.strip() != ""]

		try:
			if len(address) < 3:
				item['city'], item['state'], item['zip'], item['physical_address'] = "", "", "", ""
			else:
				try:
					item['zip'] = address[-1].split(" ")[1].split("-")[0]
					item['city'] = address[-2]
					item['state'] = address[-1].split(" ")[0]
					item['physical_address'] = ", ".join([address[-3], item['city'], item['state'], item['zip']])
				except:
					item['zip'] = address[-1].split("-")[0]
					item['city'] = address[-3]
					item['state'] = address[-2]
					item['physical_address'] = ", ".join([address[-4], item['city'], item['state'], item['zip']])
		except:
			print address
			print response.url

		# print json.dumps(item, indent=4)
		self.results.append(item)

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""

	def cleanhtml(self, raw_html):
		cleanr = re.compile('<.*?>')
		cleantext = re.sub(cleanr, '', raw_html)
		return cleantext