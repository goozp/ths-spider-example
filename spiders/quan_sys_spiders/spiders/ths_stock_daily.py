# -*- coding: utf-8 -*-
import scrapy
import json

from quan_sys_spiders.items.stock import StockDetailItem
from quan_sys_spiders.tools.jsonp import from_jsonp
from quan_sys_spiders.tools.mongodb import MongoInstance

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ThsStockDailySpider(scrapy.Spider):
    name = 'ths-stock-daily'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS' : {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'd.10jqka.com.cn',
            'Referer': 'http://stockpage.10jqka.com.cn/realHead_v2.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        },
        'DOWNLOADER_MIDDLEWARES' : {
            'quan_sys_spiders.middlewares.proxy.xdl.ProxyMiddleware': 555,
        },
        'ITEM_PIPELINES' : {
            'quan_sys_spiders.pipelines.ths_pipelines.TimePipeline': 300,
            'quan_sys_spiders.pipelines.ths_pipelines.ThsMongoDailyPipeline': 301,
        }
    }
    
    allowed_domains = ['stockpage.10jqka.com.cn']

    # start_stock_detail = 'http://stockpage.10jqka.com.cn/{code}/'
    start_stock_detail = 'http://d.10jqka.com.cn/v2/realhead/hs_{code}/last.js'

    def start_requests(self):
        result = self.check_code()
        if result:
            for item in result:
                yield scrapy.Request(
                self.start_stock_detail.format(code=item['code']),
                callback = self.parse_stock_detail,
                meta={'code': item['code']},
                errback = self.errback_ths
            )

    def check_code(self):
        self.logger.info("股票代码已更新，开始更新股票当日数据。")
        # 查询股票code
        mongo_host = self.settings.get('MONGO_URI')
        mongo_db = self.settings.get('MONGO_DATABASE_STOCK')
        mongo = MongoInstance(mongo_host, mongo_db)
        result = mongo.find('stock', {}, {'_id': 0, 'code': 1})
        mongo.close()
        return result
        
    def parse_stock_detail(self, response):
        self.logger.info("Visited %s", response.url)

        code = str(response.meta['code'])
        callback_name = 'quotebridge_v2_realhead_hs_'+code+'_last'
        result = from_jsonp(response.text, callback_name)
        if result.get('items'):
            items = result.get('items')
            stock_daily = StockDetailItem()
            stock_daily['code'] = items['5']
            stock_daily['name'] = items['name']
            stock_daily['update_time'] = items['updateTime']
            stock_daily['yest_close_price'] = items['6']
            stock_daily['today_open_price'] = items['7']
            stock_daily['today_highest_price'] = items['8']
            stock_daily['today_lowest_price'] = items['9']
            stock_daily['today_close_price'] = items['10']
            stock_daily['today_volume'] = items['10']
            stock_daily['today_turnover'] = items['19']
            stock_daily['today_upper_limit'] = items['69']
            stock_daily['today_lower_limit'] = items['70']
            stock_daily['amplitude'] = items['526792']
            stock_daily['pb_ratio'] = items['592920'] # 市净率 %
            stock_daily['pe_ratio'] = items['2034120'] # 市盈率(动) %
            stock_daily['turnover_rate'] = items['592920'] # 换手率 % 
            stock_daily['market_capitalization'] = items['3475914'] # 流通市值
            stock_daily['total_capitalization'] = items['3541450'] # 总市值
            stock_daily['quote_change'] = items['199112'] # 涨跌幅
            stock_daily['price_change'] = items['264648'] # 价格变动
            yield stock_daily

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