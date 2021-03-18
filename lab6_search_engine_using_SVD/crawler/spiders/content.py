import scrapy
from scrapy.loader import ItemLoader
import re
import time

class SpiderContent(scrapy.Spider):
    name = "content"
    counter = 0

    def start_requests(self):
        links = open('links.txt', 'r')
        for line in links:
            yield scrapy.Request(url=line, callback=self.parse)


    def parse(self, response):
        file_name = response.url.split("/")[3]
        f = open(f'files/{file_name}.txt', 'w+', encoding='utf-8')
        for p in response.xpath("//div[@class = 'entry-content']/p"):
            p = p.extract()
            clean = re.compile('<.*?>')
            p = re.sub(clean, '', p)
            f.write(p)

        time.sleep(0.4)
        for p in response.xpath("//div[@class = 'entry-content']/blockquote/p"):
            p = p.extract()
            clean = re.compile('<.*?>')
            p = re.sub(clean, '', p)
            f.write(p)

        file_name = file_name.replace("-", " ")
        f.write(" " + file_name)
        f.close()