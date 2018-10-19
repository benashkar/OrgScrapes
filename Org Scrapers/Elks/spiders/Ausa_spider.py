import scrapy
import json

from selenium import webdriver
import time
from lxml import html
import json

class AusaSpider(scrapy.Spider):
	name = "ausa"
	base_url = "https://www.ausa.org/search/chapters?f%5B0%5D=field_addr%253Acountry%3AUS"
	domain = "https://www.ausa.org"

	header = {
		"cache-control": "max-age=0",
		"cookie": "__cfduid=dfb54cf31224b026d180797de427a8cd71538592451; _ga=GA1.2.1886058461.1538592453; __qca=P0-1620180668-1538592453693; has_js=1; _gid=GA1.2.342574495.1538850691; _dc_gtm_UA-33873687-1=1",
		"upgrade-insecure-requests": "1",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
	}

	def __init__(self):
		self.results = []
		self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
		self.details = []
		self.testtp = open("test.txt", "wb")

	def start_requests(self):
		yield scrapy.Request(url=self.base_url, 
			meta={"page": 0}, headers=self.header,
			callback=self.parse_list)

	def parse_list(self, response):
		page = response.meta['page']

		posts = response.xpath("//div[contains(@class, 'views-row')]//h2[@class='field-content']//a/@href").extract()

		for post in posts:
			self.details.append(self.domain+post)

		page += 1
		if page >= 6:
			yield scrapy.Request(url=self.details[0], headers=self.header, meta={'index': 0}, callback=self.parse_detail, dont_filter=True)
			return

		yield scrapy.Request(url=self.base_url + "&page=%d" % page, 
			meta={"page": page}, headers=self.header,
			callback=self.parse_list)

	def parse_detail(self, response):
		index = response.meta['index']
		item = dict()
		item['post_name'] = ("Association of the U.S Army " + self.validate(response.xpath("//a[@class='active']/text()"))).strip()
		street = self.validate(response.xpath("//div[@class='street-block']//div/text()"))
		locality = self.validate(response.xpath("//span[@class='locality']/text()"))
		state = self.validate(response.xpath("//span[@class='state']/text()"))
		postal_code = self.validate(response.xpath("//span[@class='postal-code']/text()"))
		country = self.validate(response.xpath("//span[@class='country']/text()"))

		item['address'] = ", ".join([tp for tp in [street, locality, state+" "+postal_code, country] if tp!=""])
		item['phone'] = self.validate(response.xpath("//div[@class='chapter-field chapter-phone']//a[contains(@href,'tel:')]/text()"))
		item['website'], item['facebook'], item['email'] = "", "", ""
		links = response.xpath("//div[@class='chapter-field chapter-links']//a")
		for link in links:
			title = self.validate(link.xpath("./text()"))
			if "Website" in title:
				item['website'] = self.validate(link.xpath("./@href"))
			if "Facebook" in title:
				item['facebook'] = self.validate(link.xpath("./@href"))
			if "Email" in title:
				self.driver.get(response.url)
				time.sleep(1)
				source = self.driver.page_source.encode("utf8")
				tree = html.fromstring(source)
				email_tp = tree.xpath("//div[@class='chapter-field chapter-links']//a")
				for tp in email_tp:
					if tp.xpath("./text()")[0].strip() == "Chapter Email":
						item['email'] = tp.xpath("./@href")[0].replace("mailto:", "")

		self.results.append(item)

		index += 1
		if index >= len(self.details):
			return

		print "index - %d" % index
		self.testtp.write("index - %d" % index)
		yield scrapy.Request(url=self.details[index], headers=self.header, meta={'index': index}, callback=self.parse_detail, dont_filter=True)

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""