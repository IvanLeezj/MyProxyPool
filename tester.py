# 检测模块
import asyncio
from asyncio import TimeoutError
import aiohttp
try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError

from db import RedisClient
from setting import *


class Tester():

    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []
        self._conn = RedisClient()

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies

    async def test_single_proxy(self, proxy):
        """
        检测单个代理
        :param proxy:
        :return:
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    real_proxy = 'http://'+proxy
                    print("Testing proxy:", proxy)
                    async with session.get(url=self.test_api, proxy=real_proxy, timeout=GET_PROXY_TIME) as response:
                        if response.status == 200:
                            print("Valid proxy:", proxy)
                            self._conn.max(proxy)
                        else:
                            print("Invalid proxy:", proxy)
                            self._conn.decrease(proxy)
                except (ProxyConnectionError, TimeoutError, ValueError) as e:
                    print("Invalid proxy", proxy)
                    self._conn.decrease(proxy)
        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError) as e:
            print('-----ConnectionError ServerDisconnectedError ClientConnectorError--------')

    def run(self):
        print('-------------Tester is working------------------')
        try:
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
        except:
            print("---------------------Async Error---------------------")


if __name__ == '__main__':
    test = Tester()
    test._raw_proxies = ['103.122.107.122:8080']
    test.run()






