from selenium import webdriver
from selenium.webdriver.common.keys import Keys #Get the keys like enter button etc.
from selenium.webdriver.chrome.options import Options #to create a headless browser(it will not appear)
from shutil import which

#Create a headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")

#Insert the chromedriver.exe
chrome_path = which("chromedriver")

#executable_path="path of chromedriver.exe" if the previous is not used
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
driver.get("https://duckduckgo.com")


#driver.find_elements_by_class_name("")
#driver.find_elements_by_tag_name()
#driver.find_elements_by_css_selector
#driver.find_element_by_id("search_form_input_homepage")
search_input = driver.find_element_by_xpath("(//input[contains(@class, 'js-search-input')])[1]")
search_input.send_keys("My User Agent")

#Those 2 lines are to select and click the button
#search_btn = driver.find_element_by_id("search_button_homepage")
#search_btn.click()

#Just press enter
search_input.send_keys(Keys.ENTER)

#To output the html when  headless browser
print(driver.page_source)



#Always close the driver at the end
driver.close()
