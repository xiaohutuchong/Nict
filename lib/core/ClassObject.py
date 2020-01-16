# 插件写法模板
class Auxiliary(object):
    def __init__(self):
        """定义插件属性"""
        pass

    def verify(self, args):
        """
        验证poc
        :return:
        """
        pass

    def attack(self, args):
        """
        利用POC
        :return:
        """
        pass


class Discover(object):
    def __init__(self):
        """定义插件属性"""
        self.description = ''

    def start_up(self, args):
        """定义启动方法"""
        pass

    def simple_task(self, args):
        """添加普通任务"""
        pass

    def thread_task(self, args):
        """添加线程任务"""
        pass
