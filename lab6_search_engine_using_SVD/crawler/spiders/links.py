import scrapy

class SpiderLinks(scrapy.Spider):
    start_urls = ['http://ww2today.com/']
    name = "links"

    def parse(self, response):
        f = open('links.txt', 'a+')
        for links in response.xpath("//main/article/header/h2[@class = 'entry-title']"):
            f.write(links.xpath(".//a/@href").extract_first() + '\n')

        next_page = response.xpath("//div[@class = 'nav-links']/a[@class = 'next page-numbers']/@href").extract_first()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)

