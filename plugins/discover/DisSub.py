# -*-* coding:UTF-8
import re
from lib.core import Global
from lib.core.ClassObject import Discover
from lib.requests.Requests import Requests
from concurrent.futures.thread import ThreadPoolExecutor


class DiscoverModule(Discover):
    def __init__(self):
        super().__init__()
        self.description = '收集目标站点的下级域名'

    def start_up(self, target):
        with ThreadPoolExecutor(max_workers=Global.Options['threads']) as executor:
            result_list = [executor.submit(_, target['domain']).result() for _ in [self.cert_search, self.threatcrowd_search, self.securitytrails_search]]
        return 'subdomains', list(set(sum(result_list, [])))

    @staticmethod
    def cert_search(arg):
        search_url = 'https://crt.sh/?q=%25.{}'.format(arg)
        response = Requests.get(search_url)
        search_result = re.findall('<TD>(.*?'+arg+')</TD>', response.text)
        return search_result

    @staticmethod
    def virustotal_search(arg):
        result_list = []
        search_url = 'https://www.virustotal.com/ui/domains/{}/subdomains'.format(arg)
        response = Requests.get(search_url)
        result_list.append(_['id'] for _ in response.json()['data'] if _['type'] == 'domain')
        return result_list


    @staticmethod
    def threatcrowd_search(arg):
        search_url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={}'.format(arg)
        response = Requests.get(search_url)
        return response.json()['subdomains']


    @staticmethod
    def securitytrails_search(arg):
        search_url = 'https://api.securitytrails.com/v1/domain/{}/subdomains?apikey=qiVWdvg42nHIYqsaL3nAmtK8BpasOVaK'.format(arg)
        response = Requests.get(search_url)
        result_list = list(map(lambda x: x + '.' + arg, response.json()['subdomains']))
        return result_list

