# Scrapes the names of the main courses of Data Analytics from W3Schools, and prints their count

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