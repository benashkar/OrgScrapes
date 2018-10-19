import scrapy
import json
from string import ascii_lowercase
import re

class IowarealtorsSpider(scrapy.Spider):
	name = "iowarealtors"
	base_url = "https://www.iowarealtors.com/api/Ramco/MemberDirectory"
	search_url = "https://www.iowarealtors.com/members/member-directory/member-landing?id=%s"
	
	data = {
		'city': '',
		'lname': '',
		'fname': '',
		'alpha': '',
		'surrounding': 'false',
		'start': '0',
		'end': '20000'
	}
	header = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en-US,en;q=0.9',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Cookie': '_ga=GA1.2.343258354.1539725064; ASP.NET_SessionId=rbfqrwp40rsyheqik2b4hs4n; _gid=GA1.2.1293995706.1539849970; _gat=1; __atuvc=6%7C42; __atuvs=5bc83ef86f839dc6000',
		'Host': 'www.iowarealtors.com',
		'Origin': 'https://www.iowarealtors.com',
		'Referer': 'https://www.iowarealtors.com/members/member-directory',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest'
	}
	def __init__(self):
		self.results = []

	def start_requests(self):
		yield scrapy.FormRequest(url=self.base_url,
					formdata=self.data, headers=self.header,
					callback=self.parse)

	def parse(self, response):
		realtors = json.loads(response.body)['data']['members']
		for realtor in realtors:
			yield scrapy.Request(url=self.search_url % realtor['id'], 
				meta={'address': realtor['citystate']},
				callback=self.parse_detail)

	def parse_detail(self, response):
		item = dict()
		item['name'] = self.validate(response.xpath("//h2/text()"))
		address = response.xpath("//div[@class='content cms-content']//p/text()").extract()
		item['address'] = []
		item['city'] = response.meta['address'].split(",")[0].strip()
		item['state'] = response.meta['address'].split(",")[1].strip()
		item['zip'] = 0
		for val in address:
			item['address'].append(val.strip())
			if "," in val and item['state'] in val:
				item['zip'] = val.strip().split(" ")[-1].split("-")[0].strip()
				break
		item['address'] = ", ".join(item['address'])
		match = re.search(r'[\w\.-]+@[\w\.-]+', response.body)
		item['email'] = match.group(0)
		try:
			ph = re.findall(r'\d{3}-\d{3}-\d{4}', response.body)
			index = 0
			while ph[index] in ["800-532-1515", "515-453-1064"]:
				index += 1
			item['phone'] = ph[index]
		except:
			item['phone'] = ''

		print json.dumps(item, indent=4)
		self.results.append(item)

	def parse_phone(self, response):
		print "============================================"
		item = response.meta
		try:
			item['phone'] = re.findall(r'\d{3}-\d{3}-\d{4}', response.body)[0]
		except:
			item['phone'] = ""
		print json.dumps(item, indent=4)
		self.results.append(item)

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""