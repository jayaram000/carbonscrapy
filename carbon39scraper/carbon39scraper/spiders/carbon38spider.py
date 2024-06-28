import scrapy 
from bs4 import BeautifulSoup
import re

class CarbonSpider(scrapy.Spider):
    name = 'carbon'
    start_urls = [' https://www.carbon38.com/shop-all-activewear/tops',
                'https://carbon38.com/collections/leggings?filter.p.m.custom.available_or_waitlist=1',
                'https://carbon38.com/collections/skirts-shorts?filter.p.m.custom.available_or_waitlist=1',
                'https://carbon38.com/collections/sports-bras?filter.p.m.custom.available_or_waitlist=1',
                'https://carbon38.com/collections/sweatshirts-hoodies?filter.p.m.custom.available_or_waitlist=1'
                'https://carbon38.com/collections/bottoms?filter.p.m.custom.available_or_waitlist=1',
                'https://carbon38.com/collections/sweaters-knits?filter.p.m.custom.available_or_waitlist=1',
                ]


    def parse(self,response):
        for product in response.css('div.ProductItem'):
            product_link = product.css('h2.ProductItem__Title a::attr(href)').get()

            if product_link:
                yield response.follow(product_link, self.parse_product)

        next_page = response.css('a.Pagination__NavItem.Link.Link--primary').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)

            
    def parse_product(self,response):
        script_content = response.xpath('//script[contains(., "var product = [{")]/text()').get()

        # Find SKU and product ID using regex
        sku_match = re.search(r"'sku'\s*:\s*\"(.*?)\"", script_content)
        product_id_match = re.search(r"'id'\s*:\s*(\d+)", script_content)

        sku = sku_match.group(1) if sku_match else None
        product_id = product_id_match.group(1) if product_id_match else None

        yield{
                'breadcrumbs' : response.css('ul.breadcrumb li ::text').getall(),
                'product_name' : response.css('h1.ProductMeta__Title::text').get().strip(),
                'brand' : response.css('h2.ProductMeta__Vendor a::text').get().strip(),
                'price' : response.css('span.ProductMeta__Price::text').get().strip(),
                'image_url' : "https:" + response.css('div.AspectRatio img::attr(src)').get().strip(),
                'reviews' : response.css('div.yotpo-bottom-line-basic-text::text').get().split(" ")[2] if response.css('div.yotpo-bottom-line-basic-text::text').get() else "0 Reviews",
                'colour': response.css('span.ProductForm__SelectedValue ::text').get(),
                'size' :[size.strip() for size in response.css('li.HorizontalList__Item label::text').getall() if size.strip()],
                "description":  response.css('div.Faq__AnswerWrapper span::text').get().strip() if response.css('div.Faq__AnswerWrapper span::text').get() else "No Description",
                "sku": sku,
                "product_id":product_id,

        
        }
