from scrapy import Item, Field


class StockItem(Item):
    collection = 'stock'

    code = Field()
    name = Field()
    crawled_at = Field()


class StockDetailItem(Item):
    collection = 'stock_detail'

    code = Field()
    name = Field()
    update_time = Field()
    yest_close_price = Field()
    today_open_price = Field()
    today_highest_price = Field()
    today_lowest_price = Field()
    today_close_price = Field()
    today_volume = Field()
    today_turnover = Field()
    today_upper_limit = Field()
    today_lower_limit = Field()
    amplitude = Field()
    pb_ratio = Field()
    pe_ratio = Field()
    turnover_rate = Field()
    market_capitalization = Field()
    total_capitalization = Field()
    quote_change = Field()
    price_change = Field()
    crawled_at = Field()

class StockNewsItem(Item):
    collection = 'stock_news'

    code = Field()
    title = Field()
    url = Field()
    crawled_at = Field()

class StockPubsItem(Item):
    collection = 'stock_pubs'

    code = Field()
    title = Field()
    url = Field()
    crawled_at = Field()
