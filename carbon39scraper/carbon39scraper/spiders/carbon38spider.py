import scrapy

class CarbonSider(scrapy.Spider):
    name = 'carbon'
    start_urls = [' https://www.carbon38.com/shop-all-activewear/tops']
    def parse(self,response):
        for products in response.css('div.ProductItem'):
            yield {
                'name': products.css('h3.ProductItem__Designer::text').get(),
                'price': products.css('span.ProductItem__Price::text').get().replace('$',''),
                'link': products.css('h2.ProductItem__Title a::attr(href)').get(),
            }