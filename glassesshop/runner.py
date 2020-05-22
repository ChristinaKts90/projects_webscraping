import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from glassesshop.spiders.bestsellers import    BestsellersSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(BestsellersSpider)
process.start()