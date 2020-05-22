# -*- coding: utf-8 -*-
import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath("//tbody/tr")

        for country in countries:
            name = country.xpath(".//td/a/text()").get()
            link = country.xpath(".//td/a/@href").get()
            final_link = response.urljoin(link)
            gdp =  country.xpath("(.//td)[2]/text()").get()
            population =  country.xpath("(.//tr/td)[3]/text()").get()
            yield{
                'Country':name,
                'Link': final_link,
                'Gdp' : gdp,
                'Population' : population
            }
