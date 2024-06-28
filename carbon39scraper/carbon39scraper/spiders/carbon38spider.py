import scrapy 
from bs4 import BeautifulSoup

class CarbonSpider(scrapy.Spider):
    name = 'carbon'
    start_urls = [' https://www.carbon38.com/shop-all-activewear/tops']


    def parse(self,response):
        for product in response.css('div.ProductItem'):
            product_link = product.css('h2.ProductItem__Title a::attr(href)').get()

            if product_link:
                yield response.follow(product_link, self.parse_product)

        next_page = response.css('a.Pagination__NavItem.Link.Link--primary').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

            
    def parse_product(self,response):

        yield{
                'breadcrumbs': response.css('ul.breadcrumbs li a::text').getall(),
                'name':response.css('h1.product-name::text').get().strip(),

        
        }
