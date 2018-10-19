import scrapy
import json

class IsdarSpider(scrapy.Spider):
	name = "isdar"
	base_url = "http://www.isdar.org/chapters.htm"

	def __init__(self):
		self.results = []

	def start_requests(self):
		yield scrapy.Request(url=self.base_url, callback=self.parse)

	def parse(self, response):
		chpaters = response.xpath("//center//table//tr")
		for chapter in chpaters:
			item = dict()
			item['city'] = self.clean(self.validate(chapter.xpath("./td[1]//font/text()")))
			if item['city'] == "Town Name":
				continue
			item['chapter_name'] = "Iowa DAR %s Chapter" % self.clean(self.validate(chapter.xpath("./td[2]//a//font/text()")))
			item['address'] = "%s, IA" % item['city']
			item['website'] =  self.clean(self.validate(chapter.xpath("./td[2]//a/@href")))
			item['email'] = self.validate(chapter.xpath("./td[3]//a/@href")).split("?")[0].replace('mailto:', '')

			print json.dumps(item, indent=4)
			self.results.append(item)

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""

	def clean(self, val):
		val = ''.join([i if ord(i) < 128 else ' ' for i in val])
		return " ".join(val.split()).strip()