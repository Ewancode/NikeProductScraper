import scrapy
from scrapy_splash import SplashRequest

class NikespiderSpider(scrapy.Spider):
    name = "nikespider"
    allowed_domains = ["www.nike.com"]
    start_urls = ["https://www.nike.com/gb/w/mens-tops-t-shirts-9om13znik1"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 3})

    def parse(self, response):
        for product in response.css('div.product-card'):
            ProductPrice = product.css('div[data-testid="product-price"]::text').get()
            ProductName = product.css('div.product-card__title::text').get()
            ProductURL = product.css('a.product-card__img-link-overlay::attr(href)').get()

            yield {
                'Product Name': ProductName,
                'Product Price': ProductPrice,
                'Product URL': response.urljoin(ProductURL),
            }
    
    