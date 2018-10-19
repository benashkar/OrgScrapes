import scrapy
import json

class AfaPostSpider(scrapy.Spider):
	name = "afapost"
	base_url = "http://secure.afa.org/contact_link_search.asp"
	search_url = "http://secure.afa.org/contact_links.asp?searchby=state&ent=chapter&stabbr=%s"

	def __init__(self):
		self.results = []

	def start_requests(self):
		yield scrapy.Request(url=self.base_url, callback=self.parse)

	def parse(self, response):
		states = response.xpath("//select[@name='stabbr']//option")

		for state in states:
			state_key = self.validate(state.xpath("./@value"))
			if state_key in ['all', 'AE']:
				continue

			yield scrapy.Request(url=self.search_url % state_key, 
				meta={'state': self.validate(state.xpath("./text()"))},
				callback=self.parse_detail)

	def parse_detail(self, response):
		if "No state organization" in response.body:
			return

		item = {'post_name': '', 'website': '', 'contact': '', 'email': '', 'post_type': 'state level association', 'address': ''}
		state_content = self.validate(response.xpath("//font[@size='1']//table[2]//font"))
		contents = state_content.split("<br>")
		item['post_name'] = response.meta['state'] + " Air Force Association"
		for tp in contents:
			values = tp.split("</b>")
			if "Contact" in values[0].strip():
				item['contact'] = values[1].strip()
			if "Website" in values[0].strip():
				item['website'] = values[1].split('<a href="')[1].split('">')[0].strip()
			if "E-Mail" in values[0].strip():
				item['email'] = values[1].split('mailto:')[1].split('">')[0].strip()

		self.results.append(item)
		print json.dumps(item, indent=4)

		locals_ass = response.xpath("//font[@size='1']//table[3]//tr")
		for local in locals_ass:
			local_content = self.validate(local.xpath("./td[2]//font"))
			if local_content == "":
				continue

			item = {'post_name': '', 'website': '', 'contact': '', 'email': '', 'post_type': 'local level association', 'address': ''}

			contents = local.xpath("./td[2]//font/text()").extract()
			contents = [tp.strip() for tp in contents if tp.strip()!=""]
			try:
				item['post_name'] = "-".join(contents[0].split("-")[1:]).split("(")[0].strip()
				item['address'] = contents[0].split("(")[1].replace(")", "").strip()
				item['contact'] = contents[1] if len(contents)>1 else ""
				item['email'] = self.validate(local.xpath("./td[2]//font//a/text()"))
			except:
				print contents
				item['post_name'] = self.validate(local.xpath("./td[2]//font//a[1]/text()"))
				item['address'] = contents[1][1:-1]
				item['website'] = self.validate(local.xpath("./td[2]//font//a[1]/@href"))
				item['contact'] = contents[2] if len(contents)>2 else ""
				item['email'] = self.validate(local.xpath("./td[2]//font//a[2]/text()"))

			self.results.append(item)
			print json.dumps(item, indent=4)

	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip()
		except:
			return ""
