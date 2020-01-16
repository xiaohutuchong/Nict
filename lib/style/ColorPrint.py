# -*-* coding:UTF-8
import os
from lib.core import Global


class ColorPrint(object):
    def __init__(self, message, style='info'):
        self.message = message
        self.style = style
        self._style_color_list = {'error': 'red', 'right': 'green', 'info': 'blue', 'warn': 'yellow', 'result': 'white'}
        self._style_symbol_list = {'error': '[-]', 'right': '[+]', 'info': '[i]', 'warn': '[!]', 'result': ' | '}
        self._unix_color_list = {'red': '\033[0;91m', 'green': '\033[0;92m', 'yellow': '\033[0;93m',
                                 'blue': '\033[0;94m', 'white': '\033[0;92m'}
        self._windows_color_list = {'red': 0x04, 'green': 0x0a, 'yellow': 0x0e, 'blue': 0x03, 'white': 0x0a}
        self._print()

    def _print(self):
        try:
            if Global.Options['nocolor']:
                print('\r' + self._style_symbol_list[self.style] + self.message + 50 * ' ')
            else:
                if os.name == 'nt':
                    print('\r' + str(self._unix_color_list[self._style_color_list[self.style]]) +
                          self._style_symbol_list[self.style] + '\033[0m ' + self.message + 50 * ' ')
                else:
                    print('\r' + str(self._windows_color_list[self._style_color_list[self.style]]) +
                          self._style_symbol_list[self.style] + '\033[0m ' + self.message + 50 * ' ')
            if self.style == 'error':
                os._exit(0)
        except:
            pass
