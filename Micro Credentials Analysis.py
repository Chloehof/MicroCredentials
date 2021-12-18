# requirements: install python packages

# importing all required packages, pandas, numpy, matplotlib, seaborn, requests,...
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import os
import scrapy

# importing data file CSV format, rename csv

current_dir_path = os.path.dirname(os.path.realpath(__file__))
csv = pd.read_csv(os.path.join(current_dir_path, 'JobVacanciesPerSector.csv'))

# importing data using webscraping methode
from scrapy.crawler import CrawlerProcess


class Job_Spider(scrapy.Spider):
    name = "job_spider"

    def start_requests(self):
        url = 'https://www.jobs.ie/academic_jobs.aspx'
        yield scrapy.Request(url=url, callback=self.parse_front)

    def parse_front(self, response):
        job_id = response.css('div.id')
        job_links = job_id.xpath('./a/@href')
        links_to_follow = job_links.extract()
        for url in links_to_follow:
            yield response.follow(url=url, callback=self.parse_pages)

    def parse_pages(self, response):
        job_title = response.xpath('//h1[contains(@class,"title")]/text()')
        job_title_ext = job_title.extract_first().strip()
        skills_tags = response.css('h4.chapter__title::text')
        skills_tags_ext = [t.strip() for t in skills_tags.extract()]
        dc_dict[job_title_ext] = 'job_titles_ext'

dc_dict dict()

process = CrawlerProcess()
process.crawl('job_spider')
process.start()


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


# data discovery, column names? number of columns and rows, missing values, duplicate data, primary key?
pd.set_option('display.max_rows', 50)
# data type
print(type(csv))
# CSV headers
print(csv.keys())
# shape of csv
print(csv.shape)

# data cleaning
print(csv.value_counts())
print(csv.duplicated().value_counts())
print('There are ' + str(len(csv)-len(csv.drop_duplicates())) + ' duplicate rows in the data set')
print('There are ' + str(csv.isna) + ' missing values in the data set')

# data analysis
df = pd.DataFrame(csv, columns=['Sector', 'Vacancies'])
print(df)
# data visualisation

# analysis conclusion
