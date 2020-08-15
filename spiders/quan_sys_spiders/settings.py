# -*- coding: utf-8 -*-

# Scrapy settings for quan_sys_spiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'quan_sys_spiders'

SPIDER_MODULES = ['quan_sys_spiders.spiders']
NEWSPIDER_MODULE = 'quan_sys_spiders.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'quan_sys_spiders (+http://www.yourdomain.com)'
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Encoding': 'gzip, deflate, sdch',
#     'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
#     'Connection': 'keep-alive',
#     'Host': 'm.weibo.cn',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
# }

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 下裁之后的自动延迟
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'quan_sys_spiders.middlewares.QuanSysSpidersSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'quan_sys_spiders.middlewares.ths.cookies.ThsCookiesMiddleware': 554,
#     'quan_sys_spiders.middlewares.ProxyMiddleware': 555,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     # 'quan_sys_spiders.pipelines.TimePipeline': 300,
#     # 'quan_sys_spiders.pipelines.WeiboPipeline': 301,
#     # 'quan_sys_spiders.pipelines.MongoPipeline': 302,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# 开启访问频率限制
AUTOTHROTTLE_ENABLED = True
# The initial download delay 访问开始的延迟
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies 访问之间的最大延迟
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server Scrapy并行发给每台远程服务器的请求数量
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# MONGO_URI = 'mongodb://user:password@host/db'
MONGO_URI = 'mongodb://user:userpwd@qs-mongo/stock'
MONGO_DATABASE_STOCK = 'stock'

# Redis数据库地址
# REDIS_HOST = 'localhost'
# Redis端口
# REDIS_PORT = 6379
# Redis密码，如无填None
# REDIS_PASSWORD = 'None'

# xundaili 讯代理设置（如使用）
PROXY_XDL_ORDERNO = ""
PROXY_XDL_SECRET = ""
PROXY_XDL_HOST = "forward.xdaili.cn"
PROXY_XDL_PORT = "80"

RETRY_HTTP_CODES = [401, 403, 408, 414, 500, 502, 503, 504]
