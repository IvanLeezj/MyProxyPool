import time
from multiprocessing import Process

from db import RedisClient
from getter import Getter
from tester import Tester
from api import app
from setting import *

class Schedule(object):
    @staticmethod
    def valid_proxy(cycle=VALID_CHECK_CYCLE):           # 传入定时检查时间
        """
        获取redis中代理并测试有效性
        :param cycle:
        :return:
        """
        _conn = RedisClient()
        _tester = Tester()

        while True:
            print('---------------Refreshing ip----------------')
            count = _conn.count()
            if count == 0:
                print('------------Waiting for adding new proxy------------')
                time.sleep(cycle)
                continue
            raw_proxies = _conn.all()
            _tester.set_raw_proxies(raw_proxies)
            _tester.run()
            time.sleep(cycle)

    @staticmethod
    def check_pool(cycle=POOL_LEN_CHECK_CYCLE):
        """
        如果redis中代理少于下限则从网站爬取代理
        :param lower_threshold:
        :param upper_threshold:
        :param cycle:
        :return:
        """
        _conn = RedisClient()
        _getter = Getter()
        # while True:
        #     if _conn.count() < POOL_LOWER_THRESHOLD:
        #         _getter.run()
        #     time.sleep(cycle)

        ################################
        if _conn.count() < POOL_LOWER_THRESHOLD:
            _getter.run()
        ###############################

    def run(self):
        print('Ip processing running')
        valid_process = Process(target=Schedule.valid_proxy)        # 获取并检测有用代理
        check_process = Process(target=Schedule.check_pool)         # 定时对数据库代理检测
        valid_process.start()
        check_process.start()

if __name__ == '__main__':
    print('开启代理池')
    s = Schedule()
    s.run()
    app.run()