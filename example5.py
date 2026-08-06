# Crawls a paginated quotes website, follows links to individual author pages, and extracts author details

import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import json

class Author_Spider(scrapy.Spider):
    name = 'author_spider'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow next pages
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        author_info = {
            'Name': extract_with_css('h3.author-title::text'),
            'Birthdate': extract_with_css('.author-born-date::text'),
            'Bio': extract_with_css('.author-description::text'),
        }
        print(author_info)
        yield author_info

# Run the Spider
feeds = {'FEEDS':{'author_data.json':{'format':'json','overwrite':True}}}
process = CrawlerProcess(settings=feeds)
process.crawl(Author_Spider)
process.start()

df = pd.read_json("author_data.json")
df.head()