# -*-* coding:UTF-8
import re
from lib.requests.Requests import Requests
from lib.core.ClassObject import Discover


class DiscoverModule(Discover):
    def __init__(self):
        super().__init__()
        self.description = '查询目标站点的物理位置'

    def start_up(self, target):
        result = self.simple_task(target)
        return 'physical address', result

    def simple_task(self, arg):
        if 'network address' not in arg.keys():
            from plugins.discover.DisHost import DiscoverModule
            arg['network address'] = DiscoverModule().start_up(arg)[1]
        data = {'ip': arg['network address']}
        response = Requests.post('https://www.ipip.net/ip.html', data=data)
        address = re.search('<td>地理位置</td>[\s\S*]*<span.*>(.*?)</span>[\s\S*]*<span style="float: right">', response.text).group(1)
        return address
