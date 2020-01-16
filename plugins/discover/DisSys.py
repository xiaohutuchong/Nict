# -*-* coding:UTF-8 -*-*
import re
from lib.requests.Requests import Requests
from lib.core.ClassObject import Discover


class DiscoverModule(Discover):
    def __init__(self):
        super().__init__()
        self.description = '检测目标站点的操作系统'

    def start_up(self, target):
        result = self.simple_task(target)
        return 'server system', result

    def simple_task(self, arg):
        response = Requests.get('http://' + arg['domain'])
        response.encoding = response.apparent_encoding
        target = arg['domain'].split('.')
        result = re.findall('"(http://.*' + target[-2] + '.' + target[-1] + '/.*\..*)"', response.text)[0]
        response = Requests.get(result.upper())
        if response.status_code == 200:
            return 'Windows'
        else:
            return 'Linux'

