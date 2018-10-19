import scrapy
import json

class NationwideSpider(scrapy.Spider):
	name = "navyleague"
	base_url = "http://www.navyleague.org/membership/locator.html"

	def __init__(self):
		self.results = []

	def start_requests(self):
		yield scrapy.Request(url=self.base_url, callback=self.parse)

	def parse(self, response):
		posts = response.xpath("//div[@class='locator_table']//tr")
		for post in posts:
			if self.validate(post.xpath("./@style")) != "":
				continue
			item = dict()

			a_name = self.validate(post.xpath(".//td[1]//a/text()"))
			item['council_name'] = " ".join([tp.strip() for tp in post.xpath(".//td[1]//strong/text()").extract() if tp.strip()!=""])
			item['council_name'] = " ".join([a_name, item['council_name']])
			item['council_name'] = " ".join(item['council_name'].split())
			item['website'] = self.validate(post.xpath(".//td[1]//a/@href"))
			item['address'] = self.validate(post.xpath(".//td[2]/text()"))
			item['contact'] = self.validate(post.xpath(".//td[3]/text()"))
			item['email'] = self.validate(post.xpath(".//td[4]//a/text()"))
			if item['email'] == "":
				item['email'] = self.validate(post.xpath(".//td[4]/text()"))

			self.results.append(item)

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""