import scrapy
import csv

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ["shop.adidas.jp"]
    start_urls = [
        "https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops&page=1",
        "https://shop.adidas.jp/item/?gender=mens&category=wear&group=bottoms&page=1",
        "https://shop.adidas.jp/item/?gender=mens&category=footwear&group=sneakers&page=1"
    ]

    def parse(self, response):
        # Get the URL of each product on the page
        product_links = response.css("a.image_link::attr(href)").extract()

        for product_link in product_links:
            # Follow the link to the product page and parse the data
            yield scrapy.Request(response.urljoin(product_link), callback=self.parse_product)

        # Follow the pagination links to the next page
        next_page = response.css(".next-page-link::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_product(self, response):
        # Extract the product data from the product page
        product_name = response.css(".product-name::text").extract_first().strip()
        product_description = response.css(".product-description::text").extract_first().strip()
        product_price = response.css(".product-price::text").extract_first().strip()
        product_image_url = response.css(".product-image::attr(src)").extract_first()

        # Save the product data to a CSV file
        with open("products.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([product_name, product_description, product_price, product_image_url])


# To run scrapy runspider sc.py