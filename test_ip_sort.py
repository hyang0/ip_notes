#!env python

from ip_notes import *

def test1():
    data_file = 'IP.pkl'
    load_data(data_file)
    sort_ip_dict()

def test2():
    data_file = 'IP.pkl'
    load_data(data_file)
    sort_ip_history()


if __name__ == '__main__':
    test1()
    print('#'*30)
    test2()