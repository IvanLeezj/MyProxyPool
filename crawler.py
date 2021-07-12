# 获取模块
from lxml import etree
import re
from utils import get_page


# 定义一个元类
class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class FreeCrawler(object,metaclass=ProxyMetaclass):

    def get_raw_proxies(self, callback):
        """
        获取各个网站代理
        :param callback:
        :return: proxies
        """
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_daili666(self):
        """
        获取代理666
        :param:
        :return: proxy
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(num) for num in range(1,5)]
        for url in urls:
            print("Crwaling",url)
            page_source = get_page(url)
            tree = etree.HTML(page_source)
            trs = tree.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/table//tr')
            for tr in trs[2:]:
                ip = tr.xpath('./td[1]/text()')[0]
                port = tr.xpath('./td[2]/text()')[0]
                ip_addres = ':'.join([str(ip), str(port)])
                yield ip_addres

    def crawl_kuaidaili(self):
        """
        获取快代理
        :return:
        """
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(num) for num in range(1,5)]
        for url in urls:
            print("Crwaling", url)
            page_source = get_page(url)
            ex = re.compile(r'<td data-title="IP">(.*?)</td>\s*<td data-title="PORT">(.*?)</td>')
            ip_port = ex.findall(str(page_source))
            for i, p in ip_port:
                ip_addres = ':'.join([str(i), str(p)])
                yield ip_addres

    def crawl_daili666_2(self):
        """
        获取代理666
        :param:
        :return: proxy
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(num) for num in range(6,20)]
        for url in urls:
            print("Crwaling",url)
            page_source = get_page(url)
            tree = etree.HTML(page_source)
            trs = tree.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/table//tr')
            for tr in trs[2:]:
                ip = tr.xpath('./td[1]/text()')[0]
                port = tr.xpath('./td[2]/text()')[0]
                ip_addres = ':'.join([str(ip), str(port)])
                yield ip_addres

    def crawl_kuaidaili_2(self):
        """
        获取快代理
        :return:
        """
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(num) for num in range(6,20)]
        for url in urls:
            print("Crwaling", url)
            page_source = get_page(url)
            ex = re.compile(r'<td data-title="IP">(.*?)</td>\s*<td data-title="PORT">(.*?)</td>')
            ip_port = ex.findall(str(page_source))
            for i, p in ip_port:
                ip_addres = ':'.join([str(i), str(p)])
                yield ip_addres


if __name__ == '__main__':
    craw = FreeCrawler()
    test = list(craw.crawl_daili666())
    print(test)
