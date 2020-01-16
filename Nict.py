# -*-* coding:UTF-8
import os
import sys
import click
import importlib
from lib.core import Global
from lib.banner import Banner
from configparser import ConfigParser
from lib.style.ColorPrint import ColorPrint
from lib.core.CollectInfo import CollectInfo


def list_plugins(ctx, param, value):
    """列出插件目录下所有插件"""
    if not value or ctx.resilient_parsing:
        return
    plugins = [_ for _ in os.listdir(os.path.join('plugins', 'discover')) if _.endswith(".py") and not _.startswith("_")]
    if len(plugins) == 0:
        ColorPrint('No plugin list', 'error')
    index = 0
    print('\nList all plugins:\n')
    for plugin_name in plugins:
        index += 1
        plugins_obj = importlib.import_module('plugins.discover.{}'.format(plugin_name[:-3]))
        print('\t{}:\t名称:{}\t简介:{}'.format(index, plugin_name[:-3], plugins_obj.DiscoverModule().description))
    ctx.exit()


def show_version(ctx, param, value):
    """显示程序版本"""
    if not value or ctx.resilient_parsing:
        return
    click.echo('Current version 4.0')
    ctx.exit()


@click.command()
@click.option('--input', '-i', help='从指定文件加载目标.')
@click.option('--target', '-t', help='设置信息收集的目标.')
@click.option('--force', '-f', help='强制探测站点子域名.', is_flag=True)
@click.option('--plugin', '-p', help='设置运行加载的插件.')
@click.option('--plugin-list', help='列出所有可用的插件.', is_flag=True, callback=list_plugins, expose_value=False, is_eager=True)
@click.option('--process', help='设置运行进程的数量, 默认50.', type=click.IntRange(1, 999), default=50)
@click.option('--threads', help='设置运行线程的数量, 默认200.', type=click.IntRange(1, 999), default=200)
@click.option('--timeout', help='设置超时连接的时间, 默认5.', type=click.IntRange(1, 60), default=5)
@click.option('--agent', help='设置代理UA访问站点.', default='Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)')
@click.option('--random-agent', help='使用随机的代理标识.', is_flag=True)
@click.option('--proxy', help='设置代理IP访问站点.', default=None)
@click.option('--random-proxy', help='使用随机的免费代理.', is_flag=True)
@click.option('--max-retries', help='设置访问重试的次数, 默认3.', type=click.IntRange(1, 12), default=3)
@click.option('--nocolor', '-n', help='关闭颜色打印的功能.', is_flag=True)
@click.option('--verbose', '-v', help='显示运行的详细信息.', is_flag=True)
@click.option('--output', '-o', help='输出结果到指定文件.')
@click.option('--version', help='显示当前程序的版本.', is_flag=True, callback=show_version, expose_value=False, is_eager=True)
def cli(**kwargs):
    """Easy to use internet information collection tool"""
    os.system("")
    Global.Options = kwargs
    return main()


def main():
    """程序的主函数"""
    Banner.show()
    check_environment()
    load_conf()
    CollectInfo().start_up()


def load_conf():
    """加载配置文件"""
    cfg = ConfigParser()
    cfg.read(os.path.join('conf', 'Config.ini'), encoding="utf-8-sig")
    Global.Options['port_list'] = eval(cfg.get('Plugin', 'DefaultScanPort'))
    Global.Options['cms_dict'] = cfg.get('Plugin', 'DefaultCmsDict')
    Global.Options['mid_dict'] = cfg.get('Plugin', 'DefaultMidDict')
    # 带--plugin参数 仅执行指定的插件
    if Global.Options['plugin']:
        Global.Options['discover_plugins'] = [Global.Options['plugin']]
    else:
        Global.Options['discover_plugins'] = eval(cfg.get('Plugin', 'DefaultDiscoverPlugins'))


def check_environment():
    """检查当前运行环境"""
    ColorPrint('Check the current environment', 'info')
    if sys.version_info[0] < 3:
        ColorPrint("Must be using Python 3.x", 'error')


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        raise
