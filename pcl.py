import requests
import csv
from parsel import Selector
from time import time

st = time()
# Define the base URL of your website
base_url = "https://shop.adidas.jp/"

# Define the categories of products and the number of pages for each category
categories = {
    "wear": "tops",
    "wear": "bottoms",
    "footwear": "sneakers",
}

# Define the fields that you want to scrape from the product pages
fields = ["product_name", "product_description", "product_price", "product_image_url"]

# Open a CSV file for writing
with open("products2.csv", "w", newline="", encoding="utf-8") as csvfile:
    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    # Loop through each category and page
    for category, group in categories.items():
        for page in range(1, 15):
            # Build the URL for the product category page
            category_url = base_url + f"item/?gender=mens&category={category}&group={group}&page={page}"
            response = requests.get(category_url)
            soup = Selector(response.text)

            # Extract the URLs of the product pages
            product_links = soup.css("a.image_link::attr(href)").getall()
            for product_link in product_links:
                product_url = base_url + product_link
                product_response = requests.get(product_url)
                product_soup = Selector(product_response.text)

                # Extract the product data
                Category = product_soup.css("span.categoryName::text").get()
                Product_name = product_soup.css("h1::text").get()
                product_price = product_soup.css("span.price-value::text").get()
                description_title = product_soup.css("h4.heading::text").get()

                # Write the product data to the CSV file
                writer.writerow({
                    "product_name": Category,
                    "product_description": Product_name,
                    "product_price": product_price,
                    "product_image_url": description_title
                })


print(time()-st)

