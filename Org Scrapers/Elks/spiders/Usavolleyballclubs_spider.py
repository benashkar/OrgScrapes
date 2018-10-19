import scrapy
import json

class UsavolleyballclubsSpider(scrapy.Spider):
	name = "usavolleyballclubs"
	domain = "http://www.usavolleyballclubs.com/"
	search_url = "http://www.usavolleyballclubs.com/clubvolleyball.asp?page_no=%d"

	def __init__(self):
		self.results = []

	def start_requests(self):
		for index in range(1, 157):
			yield scrapy.Request(url=self.search_url%index, callback=self.parse)

	def parse(self, response):
		clubs = response.xpath("//tr")
		index = 0
		for club in clubs:
			val = self.validate(club.xpath(".//td/@class"))
			if val != "dataTD" or len(club.xpath("./td")) <2:
				continue

			item = dict()
			item['club_name'] = self.clean(self.validate(club.xpath("./td[1]//font/text()")))
			item['website'] = self.validate(club.xpath("./td[1]//a/@href"))
			if item['club_name'] == "":
				item['club_name'] = self.clean(self.validate(club.xpath("./td[1]//b/text()")))
				item['website'] = ""
			url = self.validate(club.xpath("./td[1]//a[contains(@href, 'Customer_ID=')]/@href"))
			item['contact'] = self.clean(self.validate(club.xpath("./td[2]//font/text()")))
			item['phone'] = ""
			temp = club.xpath("./td[2]/text()").extract()
			for tp in temp:
				tp = self.clean(tp)
				if 'Tel' in tp:
					item['phone'] = tp.replace('Tel:', '').strip()
			temp = self.validate(club.xpath("./td[3]/text()"))
			temp = self.clean(temp)
			item['city'] = temp.split(",")[0]
			if item['city'] == "":
				item['city'] = temp.split("(")[0].replace(",", "").strip()
			try:
				item['state'] = temp.split("(")[1].replace(")", "")
			except:
				item['state'] = temp.split(",")[1]
			index += 1
		
			yield scrapy.Request(url=self.domain+url, meta={'item': item}, callback=self.parse_detail)

	def parse_detail(self, response):
		attr_block = response.xpath("//td//table")[0]
		item = response.meta['item']
		item['email'], item['address'] = "", ""
		item['phone'] = item['phone'].replace(" ", "")
		for attr in attr_block.xpath(".//tr")[1:]:
			title = self.validate(attr.xpath(".//b/text()"))
			value = self.clean(self.validate(attr.xpath("./td[2]/text()")))

			if title == "Email":
				item['email'] = self.validate(attr.xpath("./td[2]//a/@href")).split("&")[0].replace("mailto:", "").strip()
			if title == "Address":
				item['address'] = value
			if title == "Practice Area":
				item['practice_area'] = value
			if title == "Club Type":
				item['club_type'] = value
			if title == "Player Age Range":
				item['player_age_range'] = value
			if title == "Club Volleyball Region":
				item['club _volleyball_regoin'] = value

		item['detail_url'] = response.url
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