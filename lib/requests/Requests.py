import random
import requests
import urllib3

from lib.core import Global
from requests.adapters import HTTPAdapter


class Requests(object):
    def __init__(self):
        self.session = requests.session()
        self.session.mount('http://', HTTPAdapter(max_retries=Global.Options['max_retries']))
        self.session.mount('https://', HTTPAdapter(max_retries=Global.Options['max_retries']))

    @staticmethod
    def _get_headers():
        ua = [
            'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;',  # IE9.0
            'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',  # IE8.0
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',  # IE7.0
            'Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)',  # IE6.0
            'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1',  # Firefox4.0.1–MAC
            'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',  # Firefox4.0.1–Windows
            'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11',  # Opera11.11–MAC
            'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',  # Opera11.11–Windows
            'Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)',  # 傲游（Maxthon）
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)',  # 腾讯TT
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)',  # 360浏览器
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TheWorld)',  # 世界之窗（TheWorld）3.x
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        ]
        if Global.Options['random_agent']:
            user_agent = random.choice(ua)
        else:
            user_agent = Global.Options['agent']
        headers = {
            'Accept': "*/*",
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': user_agent,
            'Connection': 'close'
        }
        return headers

    @staticmethod
    def _get_proxy():
        if Global.Options['random_proxy']:
            proxy = random.choice('')
        else:
            proxy = Global.Options['proxy']
        if proxy is None:
            proxies = None
        else:
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
            }
        return proxies

    @staticmethod
    def get(url):
        try:
            response = Requests().session.get(url, headers=Requests()._get_headers(), timeout=Global.Options['timeout'], proxies=Requests()._get_proxy())
            return response
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.InvalidURL:
            return None

    @staticmethod
    def post(url, data):
        try:
            response = Requests().session.post(url, data=data, headers=Requests()._get_headers(), timeout=Global.Options['timeout'], proxies=Requests()._get_proxy())
            return response
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.InvalidURL:
            return None

    def __del__(self):
        self.session.close()
