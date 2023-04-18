
from selenium import webdriver
from selenium.webdriver.common.by import By
from parsel import Selector

import requests



base_url = "https://shop.adidas.jp/"

section = "men/"

#  item/?gender=mens&category=footwear&group=sneakers
browser = webdriver.Chrome()

browser.get(base_url+section)

key = browser.find_element(By.CLASS_NAME, "lpc-miniTeaserCard_text")
print(key)


# session = requests.Session()

# session.max_redirects = 600



# response = session.get(base_url+section)

# html = Selector(response.text)

# keys = html.css("a.lpc-miniTeaserCard_link::attr(href)").getall()

# for key in keys:

#     url = base_url+key

#     response2 = session.get(url)

#     html2 = Selector(response2.text)

#     product = html2.css("a.image_link::attr(href)").getall()
    
#     print(product)


 