# -*- coding: utf-8 -*-
import scrapy
import json

from quan_sys_spiders.items.news import NewsItem
from quan_sys_spiders.tools.mongodb import MongoInstance

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ThsNewsSpider(scrapy.Spider):
    name = 'ths-news'
    allowed_domains = ['news.10jqka.com.cn']
    start_url = 'https://news.10jqka.com.cn/tapp/news/push/stock/?page={page}&tag={tag}&track={track}&pagesize={pagesize}'
    repeat_url = 'https://news.10jqka.com.cn/tapp/news/push/stock/?page={page}&tag={tag}&track={track}&ctime={ctime}'

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS' : {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Encoding':  'gzip',
            'Host': 'news.10jqka.com.cn',
            'Referer': 'https://news.10jqka.com.cn/realtimenews.html',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        },
        'DOWNLOADER_MIDDLEWARES' : {
            'quan_sys_spiders.middlewares.proxy.xdl.ProxyMiddleware': 555,
        },
        'ITEM_PIPELINES' : {
            'quan_sys_spiders.pipelines.ths_pipelines.TimePipeline': 300,
            'quan_sys_spiders.pipelines.ths_pipelines.ThsNewsPipeline': 301,
        }
    }

    def start_requests(self):
        ctime = self.check_time()
        if ctime == 0:
            yield scrapy.Request(
                self.start_url.format(page=1, tag='', track='website', pagesize=400),
                callback = self.prase_news,
                errback = self.errback_ths
            )
        else:
            yield scrapy.Request(
                self.repeat_url.format(page=1, tag='', track='website', ctime=ctime),
                callback = self.prase_news,
                errback = self.errback_ths
            )


    def check_time(self):
        mongo_host = self.settings.get('MONGO_URI')
        mongo_db = self.settings.get('MONGO_DATABASE_STOCK')
        mongo = MongoInstance(mongo_host, mongo_db)
        result = mongo.db['news'].find({}, {'_id': 0, 'ctime': 1}).sort("ctime", -1).limit(1)
        ctime = 0
        for time in result:
            ctime = time['ctime']
        mongo.close()
        return ctime

    def prase_news(self, response):
        self.logger.info("Visited %s", response.url)

        results = json.loads(response.text)
        if results['code'] == '200':
            data = results['data']
            if int(data['total']) > 0:
                for item in data['list']:
                    news = NewsItem()
                    news['title'] = item['title']
                    news['digest'] = item['digest']
                    news['url'] = item['url']
                    news['app_url'] = item['appUrl']
                    news['important'] = 0 if item['color']=='1' else 1
                    news['ctime'] = item['ctime']
                    news['rtime'] = item['rtime']
                    news['stock'] = []
                    news['tags'] = []
                    if item['stock']:
                        for stock in item['stock']:
                            news['stock'].append({
                                'code': stock['stockCode'],
                                'name': stock['name'],
                            })
                    if item['tagInfo']:
                        for tag in item['tagInfo']:
                            news['tags'].append({
                                'name': tag['name'],
                                'score': tag['score'],
                            })
                    yield news

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