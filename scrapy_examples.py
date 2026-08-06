# %% [markdown]
# 
# Here are some examples of using scrapy to parse webpages, retrieve information and follow links
# %%
!pip install scrapy
# %% [markdown]
# ### Example 1
# Extracts the text content from all paragraphs in a given HTML snippet
# %%
import scrapy
from scrapy import Selector
html = '''<html>
            <body>
              <div class="hello world">
                <p>Hello World!</p>
              </div>
              <p>Enjoy Datacamp</p>
            </body>
          </html>'''
sel = Selector(text=html)
sel.xpath('//p/text()').extract()
# %% [markdown]
# ### Example 2
# Fetches a web page, parses it, counts all HTML elements, and extracts the page title
# %%
import scrapy
from scrapy import Selector
import requests

url='https://w3schools.com'
html = requests.get(url).content

sel = Selector(text=html)

# Print out the number of elements in the HTML document
print(f"The number of elements in the HTML document: {len( sel.xpath('//*'))}")

title = sel.xpath('//title/text()').extract()
title[0]
# %% [markdown]
# ### Example 3
# Scrapes the names of the main courses of Data Analytics from W3Schools, and prints their count
# %%
import scrapy
from scrapy import Selector
import requests

url='https://w3schools.com'
html = requests.get(url).content

sel = Selector(text=html)

s = sel.css('div#tutorials_data_analytics_links_list_desktop')\
       .css('div[data-category="data_analytics"] > a:nth-of-type(1)')\
       .css(':not(span)::text').extract()
s = [i.strip() for i in s if i.strip() != '']
# %%
print(f"#courses = {len(s)}")
print(s)
# %% [markdown]
# ### Example 4
# Scrapes Data Analytics courses names and links from W3Schools using Scrapy Spider 
# (Spiders are beneficial when you need scalable, asynchronous crawling with built-in request scheduling, retries, and easy link-following across many pages.)
# %%
import scrapy

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
# %%
from scrapy.crawler import CrawlerProcess

# Initialize the dictionary of DA courses and their links
da_course_links = {'Course': [], 'URL': []}

# Run the Spider
process = CrawlerProcess()
process.crawl(Extract_DA_Courses)
process.start()
# %%
import pandas as pd
df = pd.DataFrame.from_dict(da_course_links)
df
# %% [markdown]
# ### Example 5
# Scrapes quotes, authors, and tags from a paginated website 
# %%
import scrapy
from scrapy.crawler import CrawlerProcess

class Quotes_Spider(scrapy.Spider):
  name = "quotes_spider"
  start_urls = ['http://quotes.toscrape.com/']

  def parse(self, response):
    for quote in response.css('div.quote'):
      data = {
          'Text': quote.css('span.text::text').get().strip(u'\u201c\u201d'),
          'Author': quote.css('small.author::text').get(),
          'Tags': quote.css('div.tags a.tag::text').getall(),
      }
      yield data
      # follow links to next pages
      next_page = response.css('li.next > a::attr(href)').get()
      if next_page is not None:
        """
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback=self.parse)
        """
        # response.follow supports relative URL (no need to call urljoin)
        yield response.follow(next_page, callback=self.parse)

# Run the Spider
feeds = {'FEEDS':{'quote_data.json':{'format':'json','overwrite':True}}}
process = CrawlerProcess(settings=feeds)
process.crawl(Quotes_Spider)
process.start()
# %%
import pandas as pd
import json

df = pd.read_json("quote_data.json")
df
# %% [markdown]
# ### Example 6
# Crawls a paginated quotes website, follows links to individual author pages, and extracts author details
# %%
import scrapy
from scrapy.crawler import CrawlerProcess

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
# %%
import pandas as pd
import json

df = pd.read_json("author_data.json")
df