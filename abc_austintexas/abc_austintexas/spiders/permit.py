# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector #To convert the self.html to a selectable item
from scrapy_splash import    SplashRequest
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class PermitSpider(scrapy.Spider):
    name = 'permit'
    allowed_domains = ['abc.austintexas.gov/web/permit/public-search-other?reset=true']
    start_urls = ['http://abc.austintexas.gov/web/permit/public-search-other?reset=true/']

    all_links = []
    responses = []

    def __init__(self): # Here i will do everything related to selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        #Insert the chromedriver.extend()
        chrome_path = which("chromedriver")
        #Set the driver
        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920, 1080) #max the window to fit all results in
        driver.get("http://abc.austintexas.gov/web/permit/public-search-other?reset=true")

        #Select the LTC coin tab
        postcode_tab = driver.find_element_by_id("d_1400695220655")
        postcode_tab.send_keys("78660")
        submit_tab = driver.find_element_by_name("d_1376492350341")
        submit_tab.click()

        self.html = driver.page_source

        #Now i will loop through the permits on this page to get into the link pages
        # resp1 = Selector(text=driver.page_source)
        # while resp1.xpath("//a[contains(text(),'next')][1]"):
        #     for permit_url1 in resp1.xpath("//tbody/tr/td[2]/span"):
        #         permit_url = f'https://abc.austintexas.gov/{permit_url1.xpath(".//a/@href").get()}'
        #         #driver.get(permit_url)
        #         #print(driver.page_source)
        #         self.all_links.append(permit_url)   
        #     if len(driver.find_elements_by_xpath("//a[contains(text(),'next')][1]"))>0:
        #         next_page = driver.find_element_by_xpath("//a[contains(text(),'next')][1]")
        #         next_page.click()     
        #         resp2 = Selector(text=driver.page_source)       
        #     if len(driver.find_elements_by_xpath("//a[contains(text(),'next')][1]"))==0:
        #     #if resp2.xpath("//a[contains(text(),'next')][1]"):
        #         print('ALL OK!!!!!!!!!!!!!!!!!!!!!!')   

        #         for permit_url1 in resp2.xpath("//tbody/tr/td[2]/span"):
        #             permit_url = f'https://abc.austintexas.gov/{permit_url1.xpath(".//a/@href").get()}'
        #             #driver.get(permit_url)
        #             #print(driver.page_source)
        #             self.all_links.append(permit_url)     
        #         print('ALL OK')      
        resp1 = Selector(text=driver.page_source)
        while resp1.xpath("//a[contains(text(),'next')][1]"):
            self.all_links.append(resp1.xpath("//tbody/tr/td[2]/span/a/@href").getall())

            if len(driver.find_elements_by_xpath("//a[contains(text(),'next')][1]"))>0:
                next_page = driver.find_element_by_xpath("//a[contains(text(),'next')][1]")
                next_page.click()
            if len(driver.find_elements_by_xpath("//a[contains(text(),'next')][1]"))<1:
                resp1 = Selector(text=driver.page_source)
                self.all_links.append(resp1.xpath("//tbody/tr/td[2]/span/a/@href").getall())


        print(self.all_links)
        for i,j in enumerate(self.all_links):
            for j in self.all_links[i]:
                driver.get(f'https://abc.austintexas.gov/{j}')
                self.responses.append(driver.page_source)
        driver.close()

    def parse(self, response):
        for resp in self.responses:
            resp2 = Selector(text=resp)

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

        
