# -*-* coding:UTF-8
import re
from lib.requests.Requests import Requests
from lib.core.ClassObject import Discover


class DiscoverModule(Discover):
    def __init__(self):
        super().__init__()
        self.description = '获取目标站点的首页标题'

    def start_up(self, target):
        result = self.simple_task([target, True])
        return 'website title', result

    def simple_task(self, args):
        response = Requests.get('{}://{}'.format('http' if args[1] else 'https', args[0]['domain']))
        if response is None:
            return None
        response.encoding = response.apparent_encoding
        if response.text is None or response.status_code == 404:
            return None
        elif response.status_code == 200:
            if re.search('<title>.*</title>', response.text, re.I):
                title = re.search('<title>(.*?)</title>', response.text, re.I).group(1)
            else:
                title = 'Not found title'
        else:
            if args[1]:
                self.simple_task([args[0], False])
            title = response.status_code
        return title

