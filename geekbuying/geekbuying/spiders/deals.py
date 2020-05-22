# -*- coding: utf-8 -*-
import scrapy


class DealsSpider(scrapy.Spider):
    name = 'deals'
    allowed_domains = ['www.geekbuying.com']
    #start_urls = ['https://www.geekbuying.com/deals/categorydeals/']

    def start_requests(self):
        yield scrapy.Request(url='https://www.geekbuying.com/deals/categorydeals/', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        })

    def parse(self, response):
        for item in response.xpath("//div[@class='flash_pro_categories clearfix']/div[@class='flash_li']"):
            yield{
                'Item name': item.xpath(".//a[@class='flash_li_link']/text()").get(),
                'Link': item.xpath(".//a[@class='flash_li_link']/@href").get(),
                'Starting_Price': item.xpath(".//div[@class='flash_li_price']/del/text()").get(),
                'Discounted_Price': item.xpath(".//div[@class='flash_li_price']/span/text()").get(),
                'Discount': item.xpath(".//div[@class='category_li_off']/text()").get()
            }

        next_page = response.urljoin(
            response.xpath("//a[@class='next']/@href").get())

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            })
