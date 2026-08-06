# Scrapes Data Analytics courses names and links from W3Schools using Scrapy Spider 
# (Spiders are beneficial when you need scalable, asynchronous crawling with built-in request scheduling, retries, and easy link-following across many pages.)

import scrapy
import pandas as pd

class Extract_DA_Courses(scrapy.Spider):
  name='course_spider'
  url='https://w3schools.com'

  def start_requests(self):
    yield scrapy.Request(url=self.url, callback=self.parse)

  def parse(self, response):
    courses = response.css('div#tutorials_data_analytics_links_list_desktop')\
                .css('div[data-category="data_analytics"] > a:nth-of-type(1)')\
                .css(':not(span)::text').extract()
    links = response.css('div#tutorials_data_analytics_links_list_desktop')\
                .css('div[data-category="data_analytics"] > a:nth-of-type(1)')\
                .css('::attr(href)').extract()
    da_course_links['Course'] = [c.strip() for c in courses if c.strip() != '']
    da_course_links['URL'] = [self.url+link for link in links]

from scrapy.crawler import CrawlerProcess

# Initialize the dictionary of DA courses and their links
da_course_links = {'Course': [], 'URL': []}

# Run the Spider
process = CrawlerProcess()
process.crawl(Extract_DA_Courses)
process.start()

df = pd.DataFrame.from_dict(da_course_links)
df.head()