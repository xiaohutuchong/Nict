# -*-* coding:UTF-8
import os
import re
import json
import hashlib
from lib.core import Global
from lib.core.ClassObject import Discover
from lib.requests.Requests import Requests
from concurrent.futures import ThreadPoolExecutor


class DiscoverModule(Discover):
    def __init__(self):
        super().__init__()
        self.description = '检测目标站点使用的CMS'

    def start_up(self, target):
        with open(os.path.join('wordlist', Global.Options['cms_dict']), 'r', encoding='utf-8') as f:
            cms_list = json.load(f)
        with ThreadPoolExecutor(max_workers=Global.Options['threads']) as executor:
            result_list = executor.map(self.thread_task, [[target, _] for _ in cms_list])
        return 'web cms', list(filter(lambda x: x is not None, result_list))

    def thread_task(self, args):
        if args[1]['staticurl']:
            url = 'http://{}{}'.format(args[0]['domain'], args[1]['staticurl'])
            response = Requests.get(url)
            if response is None:
                return None
            content = response.content
            if response.status_code == 200 and content is not None:
                if hashlib.md5(content) == args[1]['checksum']:
                    return args[1]['name']
        if args[1]['homeurl']:
            url = 'http://{}{}'.format(args[0]['domain'], args[1]['homeurl'])
            response = Requests.get(url)
            if response is None:
                return None
            content = response.text
            if response.status_code == 200 and content is not None:
                if re.search(args[1]['keyword'], content, re.IGNORECASE):
                    return args[1]['name']
