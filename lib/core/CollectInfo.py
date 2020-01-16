# -*-* coding:UTF-8 -*-*
import os
import re
import sys
import time
import pandas
import importlib
from lib.core import Global
from multiprocessing import Lock
from multiprocessing.dummy import Pool
from lib.style.ColorPrint import ColorPrint


class CollectInfo(object):
    def __init__(self):
        self.lock = Lock()
        # 定义存储数据变量类型
        Global.Information = []

    @staticmethod
    def pre_pro():
        """参数值预处理"""

        if Global.Options['input']:
            with open(Global.Options['input'], 'r') as f:
                target_list = [{'domain': _.strip(), 'id': index} for index, _ in enumerate(f.readlines())]
        else:
            """检查输入内容是否正确"""
            if not re.match(r'^[\w.]*\.[\w]+$', Global.Options['target']):
                ColorPrint('Format is incorrect', 'error')
            target_list = [{'domain': Global.Options['target'], 'id': 0}]
        return target_list

    def start_up(self):
        # 获得起始时间
        start = time.time()
        # 调用发现模块探测目标信息
        self.discover_module(self.pre_pro())
        # 漏洞扫描(未完成)
        # 将收集的信息写入文件 生成信息收集报告
        self.generate_report()
        # 获得终止时间
        stop = time.time()
        # 显示结束语 计算程序运行时间
        ColorPrint('Thanks for using this tool ..End/{}s'.format(round(stop - start, 2)), 'info')

    def discover_module(self, target_list):
        with Pool(Global.Options['process']) as p:
            p.map(self.discover_plugin_task, target_list)
        # 数据整理分析
        self.analyse_discover_data()

    def discover_plugin_task(self, target):
        with self.lock:
            # PS:target_list = [{key:value}]
            ColorPrint('Start scan {}'.format(target['domain']), 'right')
            for filename in Global.Options['discover_plugins']:
                plugin_name = os.path.splitext(filename)[0]
                plugins_obj = importlib.import_module('plugins.discover.{}'.format(plugin_name))
                sys.stdout.write('\r[-] Please wait a moment..')
                try:
                    key, value = plugins_obj.DiscoverModule().start_up(target)

                except KeyError:
                    continue
                if self.check_value(key, value):
                    break
                if isinstance(value, list):
                    if len(value) == 0:
                        continue
                elif key is None or value is None:
                    continue
                self.show_info(key, value)
                target[key] = value
            if 'subdomains' in target.keys() and Global.Options['force']:
                Global.Options['force'] = False
                self.discover_module([{'domain': _} for _ in target['subdomains']])
            if len(target.keys()) > 2:
                Global.Information.append(target)

    @staticmethod
    def check_value(key, value):
        """判断当前目标是否可以丢弃"""
        if not Global.Options['plugin']:
            if key == 'network address' and value is None:
                return True
            if key == 'open port' and len(value) == 0:
                return True
        else:
            return False

    @staticmethod
    def show_info(key, value):
        """输出信息的格式"""
        if isinstance(value, list):
            if Global.Options['verbose']:
                for _ in value:
                    ColorPrint('Found {} => {}'.format(key, _), 'result')
            else:
                if len(value) < 7:
                    ColorPrint('Found {} => {}'.format(key, ', '.join(value)), 'result')
                else:
                    ColorPrint('Found {} => {}'.format(key, ', '.join(value[:6]) + '...'), 'result')
        else:
            ColorPrint('Found {} => {}'.format(key, value), 'result')

    @staticmethod
    def analyse_discover_data():
        """将同ip域名放一起 确定网段 # 信息收集整理 确定调用哪个脚本扫描(未完成)"""
        Global.Information = pandas.DataFrame(Global.Information)
        # 检查是否搜集到信息
        if len(list(Global.Information)) == 0:
            ColorPrint('Nothing not found', 'error')
        if 'network address' in list(Global.Information):
            Global.Information.set_index(['id', 'network address'])
        else:
            Global.Information.set_index(['id', 'domain'])

    @staticmethod
    def generate_report():
        """输出报告"""
        del Global.Information['id']
        if Global.Options['output'] is None:
            if not os.path.exists('output'):
                os.makedirs('output')
            Global.Options['output'] = os.path.join('output', 'result_{:.0f}.xlsx'.format(time.time()))
        ext = Global.Options['output'].split('.')[-1]
        if ext == 'xlsx':
            Global.Information.to_excel(Global.Options['output'], encoding='utf-8', index=False, header=True)
        elif ext == 'csv':
            Global.Information.to_csv(Global.Options['output'], encoding='utf-8', index=False, header=True)
        elif ext == 'txt':
            Global.Information.to_csv(Global.Options['output'], encoding='utf-8', seq='\t')
        else:
            ColorPrint('Invalid save file type', 'error')
        ColorPrint('Saving results to file: {}'.format(Global.Options['output']), 'info')
