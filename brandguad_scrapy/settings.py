BOT_NAME = "brandguad_scrapy"

SPIDER_MODULES = ["brandguad_scrapy.spiders"]
NEWSPIDER_MODULE = "brandguad_scrapy.spiders"

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# ROTATING_PROXY_LIST_PATH = "../proxies.txt"
# NUMBER_OF_PROXIES_TO_FETCH = 15


# DOWNLOADER_MIDDLEWARES = {
#     "rotating_free_proxies.middlewares.RotatingProxyMiddleware": 610,
#     "rotating_free_proxies.middlewares.BanDetectionMiddleware": 620,
# }
