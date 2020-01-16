# -*-* coding:UTF-8
from lib.requests.Requests import Requests
from lib.core.ClassObject import Discover


class DiscoverModule(Discover):
    def __init__(self):
        super().__init__()
        self.description = '检测目标站点是否有CDN'

    def start_up(self, target):
        result = self.simple_task(target)
        return 'is cdn', result

    def simple_task(self, arg):
        ip_list = []
        task_id = Requests.get('https://whoer.net/ping/create?pingit={}'.format(arg['domain'])).json()['taskID']
        result = Requests.get('https://whoer.net/zh/ping/result?task_id={}&servers=us1,fr1,ro1,hk1,it1,ca1,ch1,ru1,es1,uk1,de1,ua1,sg1,nl2,se2'.format(task_id)).json()
        for server in ['us1', 'fr1', 'ro1', 'hk1', 'it1', 'ca1', 'ch1', 'ru1', 'es1', 'uk1', 'de1', 'ua1', 'sg1', 'nl2', 'se2']:
            if 'ip' in eval(result[server]):
                ip_list.append(eval(result[server])['ip'])
        if len(list(set(ip_list))) > 1:
            return 'True'
        else:
            return 'False'

