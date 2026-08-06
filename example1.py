# Extracts the text content from all paragraphs in a given HTML snippet

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
print(sel.xpath('//p/text()').extract())