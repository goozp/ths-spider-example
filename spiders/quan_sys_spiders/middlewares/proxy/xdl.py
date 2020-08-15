import logging

from quan_sys_spiders.tools.proxy import xdl_proxy

class ProxyMiddleware():
    """
    动态代理
    """
    def __init__(self, orderno, secret, host, port):
        self.logger = logging.getLogger(__name__)
        self.orderno = orderno
        self.secret =secret
        self.host = host
        self.port = port

    def get_proxy(self):
        proxy, auth = xdl_proxy(self.orderno, self.secret, self.host, self.port)
        return proxy, auth

    def process_request(self, request, spider):
        # 抓取失败重试的时候才开启代理
        if request.meta.get('retry_times'):
            proxy, auth = self.get_proxy()
            self.logger.debug('使用代理: {proxy}'.format(proxy=self.host + ":" + self.port))
            request.meta['proxy'] = proxy['http']
            request.headers['Proxy-Authorization'] = auth

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            orderno = settings.get('PROXY_XDL_ORDERNO'),
            secret = settings.get('PROXY_XDL_SECRET'),
            host = settings.get('PROXY_XDL_HOST'),
            port = settings.get('PROXY_XDL_PORT')
        )