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
print(title[0])
