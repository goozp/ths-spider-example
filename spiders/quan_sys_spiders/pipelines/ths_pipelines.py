import logging
import pymongo
import time

from quan_sys_spiders.items.stock import StockItem, StockDetailItem, StockNewsItem, StockPubsItem
from quan_sys_spiders.items.news import NewsItem


class ThsMongoStockPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE_STOCK')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[StockItem.collection].create_index(
            [
                ('code', pymongo.ASCENDING)
            ]
        )

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, StockItem):
            # 数据存在即更新、数据不存在即插入
            # $set 操作符，这样我们如果爬取到了重复的数据即可对数据进行更新，同时不会删除已存在的字段，如果这里不加 $set 操作符，那么会直接进行 item 替换，这样可能会导致已存在的字段如关注和粉丝列表清空，所以这里必须要加上 $set 操作符。
            # 第三个参数我们设置为了 True，这个参数起到的作用是如果数据不存在，则插入数据。
            self.db[item.collection].update(
                {'code': item.get('code')}, 
                {'$set': item}, 
                True
            )
        return item

class ThsMongoDailyPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE_STOCK')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[StockDetailItem.collection].create_index(
            [
                ('code', pymongo.ASCENDING),
                ('update_time', pymongo.DESCENDING)
            ]
        )

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, StockDetailItem):
            self.db[item.collection].update(
                {'code': item.get('code'), 'update_time': item.get('update_time')}, 
                {'$set': item}, 
                True
            )
        return item

class ThsMongoNewsPubsPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE_STOCK')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[StockNewsItem.collection].create_index(
            [
                ('code', pymongo.ASCENDING)
            ]
        )
        self.db[StockPubsItem.collection].create_index(
            [
                ('code', pymongo.ASCENDING)
            ]
        )

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, StockNewsItem) or isinstance(item, StockPubsItem):
            self.db[item.collection].update(
                {'code': item.get('code'), 'url': item.get('url')}, 
                {'$set': item}, 
                True
            )
        return item


class ThsNewsPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE_STOCK')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[NewsItem.collection].create_index(
            [
                ('ctime', pymongo.DESCENDING)
            ]
        )

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, NewsItem):
            self.db[item.collection].update(
                {'title': item.get('title'), 'url': item.get('url')}, 
                {'$set': item}, 
                True
            )
        return item

class TimePipeline():
    def process_item(self, item, spider):
        if isinstance(item, StockDetailItem) or isinstance(item, StockItem) or isinstance(item, StockNewsItem) or isinstance(item, StockPubsItem) or isinstance(item, NewsItem):
            now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            item['crawled_at'] = now
        return item