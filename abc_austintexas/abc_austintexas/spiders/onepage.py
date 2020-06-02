import scrapy
from scrapy.selector import Selector #To convert the self.html to a selectable item
from scrapy_splash import    SplashRequest
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class OnepageSpider(scrapy.Spider):
    name = 'onepage'
    allowed_domains = ['https://abc.austintexas.gov/public-search-other?t_detail=1&t_selected_folderrsn=12482083&t_selected_propertyrsn=344530']
    start_urls = ['https://abc.austintexas.gov/public-search-other?t_detail=1&t_selected_folderrsn=12482083&t_selected_propertyrsn=344530/']



    def __init__(self): # Here i will do everything related to selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        #Insert the chromedriver.extend()
        chrome_path = which("chromedriver")
        #Set the driver
        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920, 1080) #max the window to fit all results in
        driver.get("https://abc.austintexas.gov/public-search-other?t_detail=1&t_selected_folderrsn=12482083&t_selected_propertyrsn=344530")

        self.html = driver.page_source
   

    def parse(self, response):
        resp2 = Selector(text=self.html)

        folder_details_col1 = resp2.xpath("//div[@class='group ']/div/label/span/strong/text()").getall()
        folder_details_col2 = resp2.xpath("//div[@class='group ']/div/span/text()").getall()
        folder_details = dict(zip(folder_details_col1, folder_details_col2))

        folder_info_col1 = resp2.xpath("//div[@class='repeat '][1]/table/tbody/tr/td[1]/span/text()").getall()
        folder_info_col2 = resp2.xpath("//div[@class='repeat '][1]/table/tbody/tr/td[2]/span/text()").getall()
        folder_info = dict(zip(folder_info_col1, folder_info_col2))

        property_details_row1 = resp2.xpath("//div[@class='repeat '][2]/table/thead/tr/th/span/label/span/strong/text()").getall()
        property_details_row2 = resp2.xpath("//div[@class='repeat '][2]/table/tbody/tr/td/span/text()").getall()
        property_details = dict(zip(property_details_row1, property_details_row2))

        people_details_col1 = resp2.xpath("//div[@class='repeat '][3]/table/tbody/tr/td[1]/span/text()").getall()
        people_details_col2 = resp2.xpath("//div[@class='repeat '][3]/table/tbody/tr/td[2]/span/text()").getall()
        people_details_col3 = resp2.xpath("//div[@class='repeat '][3]/table/tbody/tr/td[3]/span/text()").getall()
        people_details = {
            'People Type' : people_details_col1,
            'Name / Address' : people_details_col2,
            'Phone' : people_details_col3
        }

        folder_fees_col1 = resp2.xpath("//div[@class='repeat '][4]/table/tbody/tr/td[1]/span/text()").getall()
        folder_fees_col2 = resp2.xpath("//div[@class='repeat '][4]/table/tbody/tr/td[2]/span/text()").getall()
        folder_fees_col3 = resp2.xpath("//div[@class='repeat '][4]/table/tbody/tr/td[3]/span/text()").getall()
        folder_fees = {
            'Fee Description' : people_details_col1,
            'Fee Amount' : people_details_col2,
            'Balance' : people_details_col3
        }

        processes_row1 = resp2.xpath("//div[@class='repeat '][5]/table/thead/tr/th/span/label/span/text()").getall()
        processes_row2 = resp2.xpath("//div[@class='repeat '][5]/table/tbody/tr/td/span/text()").getall()
        processes = dict(zip(processes_row1, processes_row2))

        yield{
             'FOLDER DETAILS': folder_details,
             'FOLDER INFO': folder_info,
             'PROPERTY DETAILS': property_details,
             'PEOPLE DETAILS': people_details,
             'FOLDER FEES': folder_fees,
             'PROCESSES AND NOTES': processes,

             }