# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import    SplashRequest

class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']


    script = '''

        function main(splash, args)
            splash.private_mode_enabled = false
            url =args.url
            assert(splash:go(url))
            assert(splash:wait(1))
  
            ltc_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
            ltc_tab[5]:mouse_click()
            assert(splash:wait(1))
            splash:set_viewport_full()
            return {
                html = splash:html(),
                png = splash:png(),
            }
        end

    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net/en", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })


    def parse(self, response):
        for currency in response.xpath("//div[contains(@class,'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield{
                'Currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'Volume (24h)': currency.xpath(".//div[2]/span/text()").get(),
                'Last price': currency.xpath(".//div[3]/span/text()").get(),
                'Change (24h)': currency.xpath(".//div[4]/span/span/text()").get(),
                'High (24h)': currency.xpath(".//div[5]/span/text()").get(),
                'Low (24h)': currency.xpath(".//div[6]/span/text()").get(),
                #'Trading Page': currency.xpath(".//div[2]/span/text()").get(), 
                'Trading Page': response.urljoin(currency.xpath(".//div[8]/a/@href").get())
            }