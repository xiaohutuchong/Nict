# -*-* coding:UTF-8
from lib.requests.Requests import Requests
from lib.core.ClassObject import Discover


class DiscoverModule(Discover):
    def __init__(self):
        super().__init__()
        self.description = '检测目标站点的脚本语言'

    def start_up(self, target):
        result = self.simple_task(target)
        return 'script language', result

    def simple_task(self, arg):
        for script in ['php', 'asp', 'aspx', 'jsp']:
            response = Requests.get('http://{}/index.{}'.format(arg['domain'], script))
            if response.status_code == 404 or response.text is None:
                continue
            if response.status_code in [200, 301]:
                return script
