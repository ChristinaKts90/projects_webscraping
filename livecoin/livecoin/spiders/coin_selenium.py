import scrapy
from scrapy.selector import Selector #To convert the self.html to a selectable item
from scrapy_splash import    SplashRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which

class CoinSpiderSelenium(scrapy.Spider): #Change this
    name = 'coin_selenium' #Change this
    allowed_domains = ['www.livecoin.net/en']
    start_urls = [
        'https://www.livecoin.net/en'
    ]


    def __init__(self): # Here i will do everything related to selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        #Insert the chromedriver.extend()
        chrome_path = which("chromedriver")
        #Set the driver
        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920, 1080) #max the window to fit all results in
        driver.get("https://www.livecoin.net/en")

        #Select the LTC coin tab
        ltc_tab = driver.find_elements_by_class_name("filterPanelItem___2z5Gb")
        ltc_tab[4].click()

        self.html = driver.page_source
        driver.close()


    def parse(self, response):
        resp = Selector(text=self.html) #Convert the self.html from selenium to text
        for currency in resp.xpath("//div[contains(@class,'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
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