import scrapy
from carbon39scraper.items import CarbonItem

class CarbonSider(scrapy.Spider):
    name = 'carbon'
    start_urls = [' https://www.carbon38.com/shop-all-activewear/tops']


    def parse(self,response):
        prdt_link = response.css('h2.ProductItem__Title a::attr(href)').get()

        for link in prdt_link:
            yield response.follow(link,self.parse_product)

        next_page = response.css('a.Pagination__NavItem.Link.Link--primary').attrib['href']

        if next_page is not None:
            yield response.follow(next_page,self.parse)

    
