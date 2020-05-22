# -*- coding: utf-8 -*-
import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    allowed_domains = ['www.glassesshop.com']
    #start_urls = ['https://www.glassesshop.com/bestsellers']

    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        })

    def parse(self, response):
        for product in response.xpath('//a[@class="pull-left"]'):
            # yield response.follow(url=product.xpath(".//@href").get(), callback=self.parse_img, meta={
            yield{
                'product_name': product.xpath(".//text()").get(),
                'product_url': product.xpath(".//@href").get(),
                'product_price': product.xpath("//div[@class='pprice col-sm-12']/descendant::span[contains(text(),'$')]/text()").get(),
                'Product_img': product.xpath("//img[@class='default-image-front']/@src").get()
            }
        next_page = response.xpath(
            "//a[@rel='next']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page,
                                 callback=self.parse,
                                 headers={
                                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                                 })
