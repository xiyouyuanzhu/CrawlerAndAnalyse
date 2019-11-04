from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
browser=webdriver.Chrome(executable_path='/usr/bin/chromedriver')

url='http://www.hao123.com'
browser.get(url)
print(browser.page_source)