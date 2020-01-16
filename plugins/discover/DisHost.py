# -*-* coding:UTF-8
import re
from lib.requests.Requests import Requests
from lib.core.ClassObject import Discover


class DiscoverModule(Discover):
    def __init__(self):
        super().__init__()
        self.description = '查询目标站点的网络地址'

    def start_up(self, target):
        result = self.simple_task(target)
        return 'network address', result

    def simple_task(self, arg):
        if re.match(r'^[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}$', arg['domain']):
            return arg['domain']
        result = Requests.get('https://host.io/api/web/{}?token=c9fbd2b09dfed4'.format(arg['domain'])).json()
        if 'error' not in result:
            return result['ip']
        else:
            result = Requests.get('https://www.virustotal.com/ui/domains/{}/resolutions'.format(arg['domain'])).json()
            return result['data'][0]['attributes']['ip_address']
