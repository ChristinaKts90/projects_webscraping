# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest, SeleniumMiddleware
from selenium.webdriver.common.keys import Keys


class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'

    def remove_characters(self,value):
        return value.strip('\\' )

        
    def start_requests(self):
        yield SeleniumRequest(
            wait_time=3,
            url = 'http://slickdeals.net/computer-deals/',
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        #driver = response.meta['driver']
        #html = driver.page_source
        #response_obj = Selector(text=html)
        items = response.xpath("//div[@class='fpItem  ']/div/div[1]")
        for item in items:
            
            yield {
                'Name':self.remove_characters(item.xpath(".//descendant::a[@class='itemTitle bp-c-link']/text()").get()),
                'Store':item.xpath(".//descendant::node()[contains(@class,'itemStore')]/text()").get(),
                'Price':item.xpath("normalize-space(.//descendant::div[contains(@class,'itemPrice')]/text())").get(),
                'Tag':item.xpath(".//descendant::span[contains(@class,'badge')]/text()").get(),
                'Url':'http://slickdeals.net' + item.xpath(".//descendant::a[@class='itemTitle bp-c-link']/@href").get()                
            }

        next_page = response.xpath("//div[@class='pagination buttongroup']/a[@data-role='next-page']/@href").get() 
        if next_page:
            yield SeleniumRequest(
            wait_time=3,
            url = f"http://slickdeals.net{next_page}",
            screenshot=True,
            callback=self.parse
        )
