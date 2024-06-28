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
                'breadcrumbs' : response.css('ul.breadcrumbs li a::text').getall(),
                'product_name' : response.css('h1.ProductMeta__Title::text').get().strip(),
                'brand' : response.css('h2.ProductMeta__Vendor a::text').get().strip(),
                'price' : response.css('span.ProductMeta__Price::text').get().strip(),
                'image_url' : "https:" + response.css('div.AspectRatio img::attr(src)').get().strip(),
                'reviews' : response.css('div.yotpo-bottom-line-basic-text::text').get().split(" ")[2] if response.css('div.yotpo-bottom-line-basic-text::text').get() else "0 Reviews",
                'colour': response.css('span.ProductForm__SelectedValue ::text').get(),
                'size' :[size.strip() for size in response.css('li.HorizontalList__Item label::text').getall() if size.strip()],
                

        
        }
