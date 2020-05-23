# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']

    script = '''

        function main(splash, args)
        splash.private_mode_enabled = false
        url = args.url
        assert(splash:go(url))
        assert(splash:wait(0.5))
        return {
            html = splash:html(),
        }
        end

    '''

    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js/', callback=self.parse, endpoint="execute", args = {
            'lua_source': self.script
        })





    def parse(self, response):
        #print(response.body)
        for quote in response.xpath("//div[@class='quote']"):
            yield{
                'Quote Text': quote.xpath(".//span[@class='text']/text()").get(),
                'Author': quote.xpath(".//span/small[@class='author']/text()").get(),
                'Tags': quote.xpath(".//div[@class='tags']/a/text()").getall()

            }
        next_page = response.urljoin(response.xpath("//li[@class='next']/a/@href").get())

        if next_page:
            yield SplashRequest(url=next_page, callback=self.parse, endpoint="execute", args = {
               'lua_source': self.script
            })
