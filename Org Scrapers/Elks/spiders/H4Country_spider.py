import scrapy
import json

class H4CountrySpider(scrapy.Spider):
	name = "h4country"
	base_url = "https://4-h.org/find/"
	search_url = "https://4-h.org/api/locations/counties/?state=%s"
	search_url_2 = "https://4-h.org/api/locations/offices/?county=%s&state=%s&radius=90"

	header = {
		'cookie':' optimizelyEndUserId=oeu1539764312324r0.4821756085898121; optimizelySegments=%7B%22752221996%22%3A%22gc%22%2C%22757032137%22%3A%22false%22%2C%22769470572%22%3A%22direct%22%7D; optimizelyBuckets=%7B%7D; _gcl_au=1.1.880889825.1539764315; _ga=GA1.2.350619174.1539764315; _gid=GA1.2.1821760904.1539764315; _vwo_uuid_v2=D3FC315FCE27F537A4DD97F7CF5C649CB|480332ebbc76d087fbda29e4faac34e1; _vis_opt_s=1%7C; _vis_opt_test_cookie=1; _vwo_uuid=D3FC315FCE27F537A4DD97F7CF5C649CB; _vwo_ds=3%3Aa_0%2Ct_0%3A0%241539764324%3A73.95252128%3A%3A%3A4_0%2C3_0; __qca=P0-1337884488-1539764316033; PHPSESSID=c63c1ff8ddff50c7ec49f34b617367ae; state=Arizona; county=Apache',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
	}

	def __init__(self):
		self.results = []
		self.fp_test = open("url.txt", "wb")

	def start_requests(self):
		yield scrapy.Request(url=self.base_url, callback=self.parse)

	def parse(self, response):
		states = response.xpath("//select[@id='states']//option/@value").extract()
		for state in states:
			if state == "":
				continue
			yield scrapy.Request(url=self.search_url%state, headers=self.header, callback=self.parse_county, meta={"state": state})

	def parse_county(self, response):
		counties = json.loads(response.body)
		for county in counties:
			if county == "status":
				continue
			county = counties[county]
			url = self.search_url_2 % (county.replace(" ", "_"), response.meta['state'])
			yield scrapy.Request(url=url, headers=self.header, callback=self.parse_list)

	def parse_list(self, response):
		data = json.loads(response.body)
		flag = 0
		for index in data:
			if index == "status":
				continue
			office = data[index]
			item = dict()
			if office['office'] != "county": #&& office['office'] == "state":
				continue
			item['county_name'] = office['title'] + ("" if office['displayOffice'] == "" else " "+office['displayOffice'])
			temp = dict()
			keys = office['meta_keys'].split("|")
			values = office['meta_values'].split("|")
			print len(keys)
			print len(values)
			for index in range(0, len(values)):
				temp[keys[index]] = values[index]

			item['state'] = temp['state'] if 'state' in temp else ''
			item['address'] = temp['address'] if 'address' in temp else ''
			item['city'] = temp['city'] if 'city' in temp else ''
			item['state']= temp['state'] if 'state' in temp else ''
			item['zip'] = temp['zip'] if 'zip' in temp else ''
			item['phone'] = temp['phone'] if 'phone' in temp else ''
			item['website'] = temp['url'] if 'url' in temp else ''

			flag = 1
			print json.dumps(item, indent=4)
			self.results.append(item)

		if flag == 0:
			self.fp_test.write(response.url + "\n")
