# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.tinydeal.com']
    # start_urls = ['https://www.tinydeal.com/specials.html'] we dont need this one now as we have the start_requests

    def start_requests(self):
        yield scrapy.Request(url="https://www.tinydeal.com/specials.html", callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        })

    # def parse(self, response):
    #    #products = response.xpath("//ul[@class='productlisting-ul']/div/li")
    #    for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
    #        yield{
    #            'Title' : product.xpath(".//a[2]/text()").get(),
    #            'Url' : response.urljoin(product.xpath(".//a[2]/@href").get()),
    #            'Starting_price' : product.xpath(".//div[2]/span[1]/text()").get(),
    #            'Final_price' : product.xpath(".//div[2]/span[2]/text()").get()
    #        }

    def parse(self, response):
        #products = response.xpath("//ul[@class='productlisting-ul']/div/li")
        for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            yield{
                'Title': product.xpath(".//a[@class='p_box_title']/text()").get(),
                'Url': response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                'Starting_price': product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'Final_price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
                'User-Agent' : response.request.headers['User-Agent']
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        yield{
            'next_page': next_page
        }

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            })
