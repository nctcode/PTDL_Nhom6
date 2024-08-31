import scrapy
from amazon1.items import Amazon1Item
from scrapy.spidermiddlewares.httperror import HttpError

class AmazoncrawlerSpider(scrapy.Spider):
    name = "amazonCrawler"
    allowed_domains = ["amazon.com"]

    def start_requests(self):
        urls=["https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A172456&ref=nav_em__nav_desktop_sa_intl_computer_accessories_and_peripherals_0_2_6_2"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.errback_httpbin)

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 503:
                self.logger.error("Received 503 response")
        
        

    def parse(self, response):
        productList = response.xpath("//div/div/div/span[@class='rush-component']/a/@href").getall()
        for productItem in productList:
            item = Amazon1Item()
            item['productUrl'] = response.urljoin(productItem)
            request = scrapy.Request(url = response.urljoin(productItem), callback = self.parseProductDetailPage)
            request.meta['dataProduct'] = item
            yield request

        next_page = response.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Next page URL: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parseProductDetailPage(self, response):
        item = response.meta['dataProduct']
        item['productName'] = response.xpath("normalize-space(string(//div/h1/span[@id='productTitle']))").get()
        item['brand'] = response.xpath("normalize-space(string(//tr[@class='a-spacing-small po-brand']/td[@class='a-span9']/span))").get()
        item['productDescription'] = response.xpath("normalize-space(string(//div[@id='productDescription']/p/span))").get()
        country_of_origin = response.xpath("//table[@id='productDetails_techSpec_section_1']//tr[th[text()=' Country of Origin ']]/td/text()").get()
        if country_of_origin:
            item['countryOfOrigin'] = country_of_origin.strip().replace('\u200e', '')
        else:
            item['countryOfOrigin'] = None
        item['price'] = response.xpath("normalize-space(string(//div/div[1]/span[@class='aok-offscreen']))").get()
        item['typicalPrice'] = response.xpath("normalize-space(string(//span/span[1]/span[2]/span/span[2]))").get()
        item['boughtInPastMonth'] = response.xpath("normalize-space(string(//span[@class='a-size-small social-proofing-faceout-title-text']/span))").get()
        item['comment'] = response.xpath("normalize-space(string(//div[4]/span/div/div[1]/span))").get()
        item['rate'] = response.xpath("normalize-space(string(//a/span[@id='acrCustomerReviewText']))").get()
        item['star'] = response.xpath("normalize-space(string(//span[1]/a/i[1]/span))").get()

        yield item

        