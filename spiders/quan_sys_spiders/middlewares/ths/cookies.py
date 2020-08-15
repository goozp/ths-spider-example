import logging
import os
import sys
import execjs

class ThsCookiesMiddleware():
    def __init__(self, js_path):
        self.logger = logging.getLogger(__name__)
        self.js_path = js_path

    @classmethod
    def from_crawler(cls, crawler):
        path = os.path.split(os.path.realpath(__file__))[0]
        js_path = os.path.join(path, "aes.min.js")
        return cls(
            js_path=js_path
        )

    def process_request(self, request, spider):
        self.logger.debug('正在获取同花顺 Cookies')
        cookies = self.get_ths_cookies()
        if cookies:
            request.cookies['v'] = cookies
            self.logger.debug('使用 Cookies: v = ' + cookies)

    def get_ths_cookies(self):
        with open(self.js_path, 'r') as f:
            jscontent = f.read()
        cookie_v = execjs.compile(jscontent).call("v")
        # cookie = 'v={}'.format(v)
        return cookie_v
        