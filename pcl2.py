
import aiofiles

from ruia import Spider, Item, TextField, AttrField


class HackerNewsItem(Item):
    Breadcumb = TextField("ul.breadcrumbList", "a")
    Category = TextField("span.categoryName")
    Product_name = TextField("h1")
    Pricing = TextField("span.price-value")
    # Image_urls = AttrField("ul.slider-list", "img",attr="src")
    Available_size = TextField("ul.sizeSelectorList", "button")
    Description_title = TextField("h4.heading")
    General_description = TextField("div.description", "div.commentItem-mainText")
    Itemized_description = TextField("div.description", "li.articleFeaturesItem")
    Tags = TextField("div.inner", "a")

class HackerNewsSpider(Spider):
    start_urls = [
    "https://shop.adidas.jp/products/HB9386/"
    ]

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=await response.text()):
            yield item

    async def process_item(self, item: HackerNewsItem):
        async with aiofiles.open('./hacker_news.txt', 'a') as f:
            await f.write(str(item.Category) + '\n')

if __name__ == '__main__':
    HackerNewsSpider.start()