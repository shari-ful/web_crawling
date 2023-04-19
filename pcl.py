import requests
import pandas as pd
from parsel import Selector
from time import time


base_url = "https://shop.adidas.jp/"


categories = {
    "wear": "tops",
    "wear": "bottoms",
    "footwear": "sneakers",
}

item_urls= [
    "https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops",
    "https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops"
    ]

data = []

def url_redirect():
    for item_url in item_urls:
        response = requests.get(item_url)
        content = Selector(response.text)


def parse():
    

    for category, group in categories.items():
        for page in range(1, 15):
            category_url = base_url + f"item/?gender=mens&category={category}&group={group}&page={page}"
            response = requests.get(category_url)
            content = Selector(response.text)

            product_links = content.css("a.image_link::attr(href)").getall()
            for product_link in product_links:
                dict_data = {}
                product_url = base_url + product_link
                product_response = requests.get(product_url)
                product_content = Selector(product_response.text)

                dict_data['Breadcumb(Category)'] = product_content.css("ul.breadcrumbList a::text").getall()
                dict_data['Category'] = product_content.css("span.categoryName::text").get()
                dict_data['Product_name'] = product_content.css("h1::text").get()
                dict_data['Pricing'] = product_content.css("span.price-value::text").get()
                dict_data['Image_urls'] = product_content.css("ul.slider-list img::attr(src)").getall()
                dict_data['Available_size'] = product_content.css("ul.sizeSelectorList button::text").getall()
                # dict_data['Sense_of_the_size']
                dict_data['Description_title'] = product_content.css("h4.heading::text").get()
                dict_data['General_description'] = product_content.css("div.description div.commentItem-mainText::text").getall()
                dict_data['Itemized_description'] = product_content.css("div.description li.articleFeaturesItem::text").getall()
                # dict_data['Rating']
                # dict_data['Number_of_review']
                # dict_data['Recommendation_rate']
                dict_data['Tags'] = product_content.css("div.inner a::text").getall()


                data.append(dict_data)

    return data


def create_csv():
    st = time()
    scraped_data = parse()
    df = pd.DataFrame(scraped_data)
    # df.to_csv('products.csv', sep='|')
    df.to_excel("output.xlsx", sheet_name='Sheet1')

    print(time()-st)

create_csv()


