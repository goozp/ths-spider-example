from scrapy import Item, Field


class NewsItem(Item):
    collection = 'news'

    title = Field()
    digest = Field()
    url = Field()
    app_url = Field()
    important = Field()
    ctime = Field()
    rtime = Field()
    stock = Field()
    tags = Field()
    crawled_at = Field()
