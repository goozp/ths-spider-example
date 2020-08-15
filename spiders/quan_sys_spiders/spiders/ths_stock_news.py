# -*- coding: utf-8 -*-
import scrapy

from quan_sys_spiders.tools.mongodb import MongoInstance
from quan_sys_spiders.items.stock import StockNewsItem, StockPubsItem

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ThsStockNewsSpider(scrapy.Spider):
    name = 'ths-stock-news'

    allowed_domains = ['stockpage.10jqka.com.cn']

    start_url = 'http://stockpage.10jqka.com.cn/{code}/news/'
    start_url_ajax = 'http://stockpage.10jqka.com.cn/ajax/code/{code}/type/news/'

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS' : {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'stockpage.10jqka.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        },
        'DOWNLOADER_MIDDLEWARES' : {
            'quan_sys_spiders.middlewares.proxy.xdl.ProxyMiddleware': 555,
        },
        'ITEM_PIPELINES' : {
            'quan_sys_spiders.pipelines.ths_pipelines.TimePipeline': 300,
            'quan_sys_spiders.pipelines.ths_pipelines.ThsMongoNewsPubsPipeline': 301,
        }
    }

    def start_requests(self):
        result = self.check_code()
        if result:
            for item in result:
                yield scrapy.Request(
                    self.start_url_ajax.format(code=item['code']),
                    headers={"Referer": 'http://stockpage.10jqka.com.cn/{code}/news/'.format(code=item['code'])},
                    callback = self.parse_stock_news,
                    meta={'code': item['code']},
                    errback = self.errback_ths
                )

    def check_code(self):
        """
        获取所有股票代码
        """
        self.logger.info("获取股票代码。")
        # 查询股票code
        mongo_host = self.settings.get('MONGO_URI')
        mongo_db = self.settings.get('MONGO_DATABASE_STOCK')
        mongo = MongoInstance(mongo_host, mongo_db)
        result = mongo.find('stock', {}, {'_id': 0, 'code': 1})
        mongo.close()
        return result

    def parse_stock_news(self, response):
        self.logger.info("Visited %s", response.url)

        # 热点新闻
        news = response.xpath('//div[@id="news"]//a')
        for new in news:
            title = new.xpath('./@title').extract_first()
            if title:
                stock_new = StockNewsItem()
                stock_new['code'] = response.meta['code']
                stock_new['title'] = title
                stock_new['url'] = new.xpath('./@href').extract_first()
                yield stock_new

        # 公司公告
        pubs = response.xpath('//div[@id="pubs"]//a')
        for pub in pubs:
            title = pub.xpath('./@title').extract_first()
            if title:
                stock_pub = StockPubsItem()
                stock_pub['code'] = response.meta['code']
                stock_pub['title'] = title
                stock_pub['url'] = pub.xpath('./@href').extract_first()
                yield stock_pub

    def errback_ths(self, failure):
        """
        request error callback function
        """
        # log all failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HTTP Error on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNS Lookup Error on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('Timeout Error on %s', request.url)