#!env python

import sys
import os

# 获取当前脚本所在目录的上一级目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)


# 将上一级目录添加到sys.path中
sys.path.insert(0, parent_dir)

from ip_notes import *

def test1():
    data_file = '../IP.pkl'
    load_data(data_file)
    sort_ip_dict()

def test2():
    data_file = '../IP.pkl'
    load_data(data_file)
    sort_ip_history()


if __name__ == '__main__':
    test1()
    print('#'*30)
    test2()
