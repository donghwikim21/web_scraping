from scrapy import Spider, Request
from manhattan.items import ManhattanItem
import re


class ManhattanSpider(Spider):
    name = 'manhattan_spider'
    allowed_domains = ['www.realtor.com']
    start_urls = ['https://www.realtor.com/realestateandhomes-search/Manhattan_NY/pg-1']
    handle_httpstatus_list = [416]

    def parse(self, response):
        # Find the total number of pages in the result so that we can decide how many urls to scrape next
        text = response.xpath('//div[@class="component_ab-sort clearfix"]/span/text()').extract_first() 
        total = re.findall('\d+', text)
        total = int(total[0]+total[1])
        number_pages = total // 43 #completed

        # List comprehension to construct all the urls of all the manhattan result urls
        result_urls = ['https://www.realtor.com/realestateandhomes-search/Manhattan_NY/pg-{}'.format(x) for x in range(1,number_pages+1)]

        # Yield the requests to different search result urls, 
        # using parse_result_page function to parse the response.
        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)


    def parse_result_page(self, response):
        # This fucntion parses the search result page.
        
        # We are looking for url of the detail page.
        details = response.xpath('//li[@class="component_property-card js-component_property-card js-quick-view "]')

        for detail in details:
            Property = detail.xpath('.//div[@class="property-type"]/text()').extract_first()
            Bed = detail.xpath('.//span[@class="data-value meta-beds"]/text()').extract_first()
            Bath = detail.xpath('.//li[@data-label="property-meta-baths"]/span/text()').extract_first()
            Sqft = detail.xpath('.//li[@data-label="property-meta-sqft"]/span/text()').extract_first()
            Price = detail.xpath('.//span[@class="data-price"]/text()').extract_first()


            item = ManhattanItem()
            item['Property']= Property
            item['Bed'] = Bed
            item['Bath'] = Bath
            item['Sqft'] = Sqft
            item['Price'] = Price

            yield item