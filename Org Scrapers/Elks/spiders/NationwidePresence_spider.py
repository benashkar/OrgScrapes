import scrapy
import json

class NationwideSpider(scrapy.Spider):
	name = "nationwide"
	base_url = "http://amvets.org/nationwide-presence/"

	def __init__(self):
		self.results = []

	def start_requests(self):
		yield scrapy.Request(url=self.base_url, callback=self.parse)

	def parse(self, response):
		json_body = json.loads(response.body.split("wpgmaps_localize_marker_data = ")[1].split("}}};")[0].strip() + "}}}")["4"]

		for key in json_body:
			post = json_body[key]
			item = dict()
			item["post_name"] = post['title']
			try:
				temp = str(int(post['title'].split(" ")[-1]))
			except:
				temp = ""

			item['post_number'] = post['title'].split("-")[-1] if temp == "" else post['title'].split(" ")[-1]
			try:
				temp = str(int(item['post_number']))
			except:
				temp = ""
			item['post_number'] = post['title'].split("-")[-1]

			item['address'] = post['address'].replace("Call For Meeting Location,", "").strip()

			item['contact_name'], item['phone'], item['email'], item['post_type'] = '', '', '', ''
			temp = post['desc'].split("<br>")
			for tp in temp:
				if 'Contact:' in tp:
					item['contact_name'] = tp.split("<b>")[1].replace("</b>", "").strip()
				if 'Phone:' in tp:
					item['phone'] = tp.replace("Phone:", "").strip()
				if 'Email:' in tp:
					print tp
					item['email'] = tp.split("\">")[1].replace("</a>", "").strip()
				if 'Post Type(s):' in tp:
					item['post_type'] = tp.replace("Post Type(s):", "").replace(",", "").strip()

			self.results.append(item)

