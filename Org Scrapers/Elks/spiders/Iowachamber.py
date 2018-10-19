import scrapy
import json
import re

class IowachamberSpider(scrapy.Spider):
	name = "iowachamber"
	base_url = "http://www.iowachamber.net/list/"
	domain = "http://www.iowachamber.net"

	def __init__(self):
		self.results = []

	def start_requests(self):
		yield scrapy.Request(url=self.base_url, callback=self.parse)

	def parse(self, response):
		states = response.xpath("//div[@id='mn-alphanumeric']//a/@href").extract()

		for state in states[1:]:
			yield scrapy.Request(url=state, callback=self.parse_list)

	def parse_list(self, response):
		orgs = response.xpath("//div[@class='mn-title']//a/@href").extract()
		for org in orgs:
			yield scrapy.Request(url=org, callback=self.parse_detail)

	def parse_detail(self, response):
		item = dict()
		item['chamber_name'] = self.validate(response.xpath("//h1/text()"))
		temp = response.xpath("//div[@id='mn-member-aboutus']//div[@class='mn-section-content']//p/text()").extract()

		temp = [tp.strip() for tp in temp if tp.strip()!=""]
		item['director_name'], item['email'] = "", ""
		print temp
		if len(temp) < 1:
			for index in range(0, len(temp)):
				if ":" in temp[index]:
					item['director_name'] = temp[index].split(":")[1].strip()
			for index in range(0, len(temp)):
				if "@" in temp[index]:
					item['email'] = temp[index]
		else:
			item['director_name'] = self.validate(response.xpath("//div[@class='mn-member-repname']/text()"))
			match = re.search(r'[\w\.-]+@[\w\.-]+', response.body)
			item['email'] = "" if match.group(0) == "info@iowachamber.net" else match.group(0)

		item['phone'] = self.validate(response.xpath("//div[@itemprop='telephone']/text()"))
		item['website'] = self.validate(response.xpath("//li[@id='mn-memberinfo-block-website']//a/@href"))
		item['city'] = self.validate(response.xpath("//span[@itemprop='addressLocality']/text()")).replace(",", "")
		item['state'] = self.validate(response.xpath("//span[@itemprop='addressRegion']/text()")).replace(",", "")
		item['zip'] = self.validate(response.xpath("//span[@itemprop='postalCode']/text()")).split("-")[0].replace(",", "")
		item['address'] = ", ".join([self.validate(response.xpath("//div[@itemprop='streetAddress']/text()")).replace(",", ""), item['city'], item['state']+" "+item['zip']]).strip()

		print json.dumps(item, indent=4)
		self.results.append(item)

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""