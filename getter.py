from db import RedisClient
from crawler import FreeCrawler
from setting import *
from error import *

class Getter():
    def __init__(self):
        self._threshold = POOL_UPPER_THRESHOLD
        self._conn = RedisClient()
        self._crawler = FreeCrawler()

    def is_over_threshold(self):
        if self._conn.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        """
        各大网站爬取代理并做测试
        :return:
        """
        print('PoolAdder is working')
        proxy_count = 0
        while not self.is_over_threshold():
            for num in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[num]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                for proxy in raw_proxies:
                    self._conn.add(proxy)
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError
