# -*-* coding:UTF-8
import socket
from lib.core import Global
from lib.core.ClassObject import Discover
from concurrent.futures import ThreadPoolExecutor


class DiscoverModule(Discover):
    def __init__(self):
        super().__init__()
        self.description = '检测目标站点的开放端口'

    def start_up(self, target):
        if 'network address' not in target.keys():
            from plugins.discover.DisHost import DiscoverModule
            target['network address'] = DiscoverModule().start_up(target)[1]
        with ThreadPoolExecutor(max_workers=Global.Options['threads']) as executor:
            result_list = executor.map(self.thread_task, [[target, port] for port in Global.Options['port_list']])
        return 'open port', list(filter(lambda x: x is not None, result_list))

    def thread_task(self, args):
        try:
            socket.setdefaulttimeout(2)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((args[0]['network address'], int(args[1])))
            s.close()
            if result == 0:
                return str(args[1])
        except socket.error:
            return None
