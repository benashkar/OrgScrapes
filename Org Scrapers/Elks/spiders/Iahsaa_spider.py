import scrapy
import json
from string import ascii_lowercase

class IahsaaSpider(scrapy.Spider):
	name = "iahsaa"
	base_url = "https://apps.iahsaa.org/secure/jrhighpublic.php"
	search_url = "https://apps.iahsaa.org/phpclasses/serviceConnector.php?object=DirLookupManager&method=lookupJrHigh&params=school;%s"

	def __init__(self):
		self.results = []

	def start_requests(self):
		for c in ascii_lowercase:
			yield scrapy.Request(url=self.search_url % c, callback=self.parse)

	def parse(self, response):
		schools = response.body.split("<result>")
		for school in schools:
			data = school.split("<detail>")

			yield scrapy.FormRequest(url=self.base_url,
					formdata={'schoolID': data[0], 'school': data[1]},
					callback=self.parse_detail)

	def parse_detail(self, response):
		attrs = response.xpath("//td//table//tr")
		temp = dict()
		for attr in attrs:
			title = self.validate(attr.xpath(".//b/text()")).replace(":", "")
			value = self.validate(attr.xpath(".//td[2]/text()"))
			if title == "Website":
				value = self.validate(attr.xpath(".//td[2]//a/text()"))
			if title == "":
				continue
			temp[title] = value

		item = dict()
		item['school_name'] = temp['School']
		item['address'] = temp['Address'].capitalize()
		item['city'] = temp['City'].capitalize()
		item['state'] = 'IA'
		item['zip'] = temp['Zip'].split("-")[0]
		item['phone'] = temp['Phone'].replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
		item['principal_name'] = temp['Principal Name']
		item['principal_phone'] = temp['Principal Phone']
		item['principal_email'] = temp['Principal Email']
		item['athletic_administrator_name'] = None if temp['Athletic Administrator Name']=="" else temp['Athletic Administrator Name']
		item['athletic_administrator_phone'] = None if temp['Athletic Administrator Phone']=="" else temp['Athletic Administrator Phone']
		item['athletic_administrator_email'] = None if temp['Athletic Administrator Email']=="" else temp['Athletic Administrator Email']
		item['vice_principal_name'] = None if temp['Vice-Principal Name']=="" else temp['Vice-Principal Name']
		item['vice_principal_phone'] = None if temp['Vice-Principal Phone']=="" else temp['Vice-Principal Phone']
		item['vice_principal_email'] = None if temp['Vice-Principal Email']=="" else temp['Vice-Principal Email']
		item['website'] = None if temp['Website']=="" else temp['Website']

		print json.dumps(item, indent=4)
		self.results.append(item)

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""