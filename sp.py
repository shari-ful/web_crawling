import csv
from pyspider.libs.base_handler import *
from pyspider.result import ResultWorker

# Define the base URL of your website
base_url = "https://www.example.com/"

# Define the categories of products and the number of pages for each category
categories = {
    "clothing": 5,
    "footwear": 4,
    "accessories": 3,
    "electronics": 4
}

# Define the fields that you want to scrape from the product pages
fields = ["product_name", "product_description", "product_price", "product_image_url"]

# Define a CSV writer class to write the scraped data to a file
class CSVWriter(object):
    def __init__(self, filename):
        self.file = open(filename, "w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(self.file, fieldnames=fields)
        self.writer.writeheader()
    def write(self, data):
        self.writer.writerow(data)
    def close(self):
        self.file.close()

# Define a PySpider handler to scrape the product data
class ProductSpider(BaseHandler):
    crawl_config = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
            "Referer": base_url
        }
    }
    result_worker = ResultWorker()

    # Define the on_start method to start crawling the website
    def on_start(self):
        # Loop through each category and page
        for category, num_pages in categories.items():
            for page in range(1, num_pages+1):
                # Build the URL for the product category page
                category_url = base_url + f"item/gender=mens&category={category}&page={page}"
                self.crawl(category_url, callback=self.parse_category)

    # Define the parse_category method to parse the product URLs from the category page
    def parse_category(self, response):
        product_links = response.doc(".product-link")
        for product_link in product_links:
            product_url = base_url + product_link.attr.href
            self.crawl(product_url, callback=self.parse_product)

    # Define the parse_product method to parse the product data from the product page
    def parse_product(self, response):
        product_name = response.doc(".product-name").text().strip()
        product_description = response.doc(".product-description").text().strip()
        product_price = response.doc(".product-price").text().strip()
        product_image_url = response.doc(".product-image").attr.src

        # Write the product data to the CSV file
        item = {
            "product_name": product_name,
            "product_description": product_description,
            "product_price": product_price,
            "product_image_url": product_image_url
        }
        self.result_worker.save_result(item, callback=self.save_item)

    # Define the save_item method to save the product data to a CSV file
    def save_item(self, result):
        writer = CSVWriter("products.csv")
        writer.write(result)
        writer.close()

# Start the PySpider instance
if __name__ == "__main__":
    ProductSpider().run()
