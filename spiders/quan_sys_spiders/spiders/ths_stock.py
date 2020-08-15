# -*- coding: utf-8 -*-
import scrapy
import json

from quan_sys_spiders.items.stock import StockItem, StockDetailItem

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class ThsStockSpider(scrapy.Spider):
    name = 'ths-stock'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS' : {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'q.10jqka.com.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        },
        'DOWNLOADER_MIDDLEWARES' : {
            'quan_sys_spiders.middlewares.ths.cookies.ThsCookiesMiddleware': 554,
            'quan_sys_spiders.middlewares.proxy.xdl.ProxyMiddleware': 555,
        },
        'ITEM_PIPELINES' : {
            'quan_sys_spiders.pipelines.ths_pipelines.TimePipeline': 300,
            'quan_sys_spiders.pipelines.ths_pipelines.ThsMongoStockPipeline': 301,
        }
    }

    allowed_domains = ['q.10jqka.com.cn']
    # start_urls = ['http://q.10jqka.com.cn/']
    start_stock = 'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{page}/ajax/1/'

    def start_requests(self):
        yield scrapy.Request(
            self.start_stock.format(page=1),
            callback = self.prase_index,
            errback = self.errback_ths
        )

    def prase_index(self, response):
        self.logger.info("Visited %s", response.url)
        # first page
        for tr_sel in response.xpath('//tbody//tr'):
            stock_item = StockItem()
            stock_item['code'] = tr_sel.xpath('./td[2]//text()').extract_first()
            stock_item['name'] = tr_sel.xpath('./td[3]//text()').extract_first()
            yield stock_item
        # begin with second page 
        page_info = response.xpath('//span[@class="page_info"]//text()').extract_first()
        total_page = int(page_info.split('/')[1])
        for page in range(2, total_page+1):
            yield scrapy.Request(
                self.start_stock.format(page=page),
                callback = self.parse_stock,
                errback = self.errback_ths
            )

    def parse_stock(self, response):
        self.logger.info("Visited %s", response.url)
        for tr_sel in response.xpath('//tbody//tr'):
            stock_item = StockItem()
            stock_item['code'] = tr_sel.xpath('./td[2]//text()').extract_first()
            stock_item['name'] = tr_sel.xpath('./td[3]//text()').extract_first()
            yield stock_item

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