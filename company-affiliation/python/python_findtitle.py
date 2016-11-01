# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# print elem.text.encode('ascii', 'ignore').decode('ascii')
# driver.quit()




from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox() # Get local session of firefox

# 0 wait until the pages are loaded
browser.implicitly_wait(3) # 3 secs should be enough. if not, increase it

browser.get("http://www.google.com") # Load page

# 1 & 2 
title = browser.title
if (title == "Google"):
	print title, len(title)

# # 3 & 4
# curre = browser.current_url
# print curre, len(curre)

# #5
# browser.refresh()

# #6
# page_source = browser.page_source
# print page_source, len(page_source)

browser.close()