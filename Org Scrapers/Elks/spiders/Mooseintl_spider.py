import scrapy
import json

class MooseintlSpider(scrapy.Spider):
	name = "mooseintl"

	base_urls = [
		"https://www.mooseintl.org/route/ajax.php?lat1=39.5431&lat2=48.22700698333404&lng1=-125.8720172780117&lng2=-123.05675651867449&rv=false&camping=false&smoke_free=false",
		"https://www.mooseintl.org/route/ajax.php?lat1=37.37212325416649&lat2=48.22700698333404&lng1=-123.05675651867449&lng2=-120.24149575933723&rv=false&camping=false&smoke_free=false",
		"https://www.mooseintl.org/route/ajax.php?lat1=33.03016976249947&lat2=48.22700698333404&lng1=-120.24149575933723&lng2=-117.42623500000002&rv=false&camping=false&smoke_free=false",
		"https://www.mooseintl.org/route/ajax.php?lat1=30.85919301666596&lat2=46.056030237500536&lng1=-117.42623500000002&lng2=-114.61097424066281&rv=false&camping=false&smoke_free=false",
		"https://www.mooseintl.org/route/ajax.php?lat1=30.85919301666596&lat2=43.88505349166702&lng1=-114.61097424066281&lng2=-111.7957134813256&rv=false&camping=false&smoke_free=false",
		"https://www.mooseintl.org/route/ajax.php?lat1=30.85919301666596&lat2=39.5431&lng1=-111.7957134813256&lng2=-108.98045272198834&rv=false&camping=false&smoke_free=false"]

	def __init__(self):
		self.results = []
		self.ids = []

	def start_requests(self):
		for url in self.base_urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		lodges = json.loads(response.body)

		for lodge in lodges['data']:
			item = dict()
			item['lodge_number'] = lodge['name'].split("-")[0].replace("#", "").strip()
			if item['lodge_number'] in self.ids:
				print "duplication - %s" % item['lodge_number']
				continue
			self.ids.append(item['lodge_number'])
			item['lodge_name'] = " ".join(lodge['name'].split("-")[1:]).strip() + " Moose Lodge"
			item['address'] = lodge['address']

			descs = lodge['description'].split("<br>")
			item['phone'], item['lodge_email'], item['chapter_email'], item['website'] = "", "", "", ""
			for desc in descs:
				if "Phone:" in desc:
					item['phone'] = desc.replace("Phone:", "").replace("(", "").replace(") ", "-").strip()
				if "Lodge Email" in desc:
					item['lodge_email'] = desc.split('">Lodge Email')[0].split("mailto:")[1].strip().split('" target=')[0]
				if "Chapter Email" in desc:
					item['chapter_email'] = desc.split('">Chapter Email')[0].split("mailto:")[-1].strip().split('" target=')[0]
				if "Website" in desc and "No Website Available" not in desc:
					item['website'] = desc.split('" target')[0].replace('<a href="', "").strip()
			
			self.results.append(item)