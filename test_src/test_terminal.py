import os
import sys
from pprint import pprint

import platform

if platform.system() == 'Windows':
    terminal = os.environ.get('TERM')
    if terminal and 'xterm' in terminal:
        sys.stdout.reconfigure(encoding='utf-8')

# 获取环境变量
pprint(os.environ)

# 修改标准输出编码为新的编码（例如，UTF-8）
#new_encoding = 'utf-8'
#sys.stdout = open(sys.stdout.fileno(), mode='w', encoding=new_encoding, buffering=1)

#sys.stdout.reconfigure(encoding='utf-8')


