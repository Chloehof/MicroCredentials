import scrapy
from scrapy.crawler import CrawlerProcess


class JOBspider(scrapy.Spider):

    name = "JOB_spider"

    def start_requests(self):
        urls = ['https://www.jobs.ie/Jobs.aspx']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        html_file = 'Job_Listings.html'
        with open(html_file, 'wb') as html_file:
            html_file.write(response.body)


print('html_file')
