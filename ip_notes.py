#!env python

import pickle
import os
import argparse
import re
import sys
import ipaddress
import platform
from pprint import pprint
import io
import wcwidth
import code

# 版本信息
version = '0.1'

# IP 字典
# 字典元素结构 ’192.168.1.1' : ['备注1’， '备注2', ...]
ip_dict = dict()

# IP 备注历史
# 集合元素结构 ('192.168.1.1', '备注1 备注2 ...')
ip_history = set()

# IP 标签
# 标签元素结构 ’192.168.1.1' : {'标签1’， '标签2', ...}
ip_tag = dict()

# 以标签为 key ， IP 为 value
# '标签1' : ['192.168.1.1', '192.168.1.2', ...]
tags = dict()

def default_ipdata():
    """默认IP数据文件
    如果没有指定数据文件，则使用默认数据文件；
    默认数据文件可能位置：
    ./IP.pkl
    ~/.ip_data/IP.pkl
    如果当前目录有数据文件，则使用当前目录数据文件 ./IP.pkl
    否则使用 ~/.ip_data/IP.pkl 作为默认数据文件
    """
    ipdata = 'IP.pkl'
    if os.path.exists(ipdata):
        return ipdata
    if platform.system() == 'Windows':
        home_dir = os.environ.get('USERPROFILE')
        ipdata = os.path.join(home_dir, '.ip_notes', 'IP.pkl')
    else:
        home_dir = os.environ.get('HOME')
        ipdata = os.path.join(home_dir, '.ip_notes', 'IP.pkl')
    if os.path.exists(ipdata):
        return ipdata
    data_folder = os.path.dirname(os.path.abspath(ipdata))
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    return ipdata


def is_ipv4(ip):
    """检查是否是IPV4"""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def foreach_set(ip_set):
    """遍历集合"""
    iterator = iter(ip_set)

    # 使用while循环和next函数遍历集合中的元素
    while True:
        try:
            element = next(iterator)
            pprint(element)
        except StopIteration:
            break


def foreach_dict(mydict):
    """遍历字典"""
    for key, value in mydict.items():
        print(f"{key}: {value}")


def load_data(file_path):
    """装载数据到字典"""
    global ip_dict, ip_history, ip_tag
    if not file_path:
        return
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            loaded_data = pickle.load(file)
            ip_dict, ip_history = loaded_data[0], loaded_data[1]
            try:
                # 新增加的字段
                ip_tag = loaded_data[2]
            except:
                pass


def save_data(file_path):
    """存盘"""
    data = [ip_dict, ip_history, ip_tag]
    # pprint(data)
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)


def insert_ip_note(file_path, enable_tag=False):
    """装载原始数据文件"""
    global ip_dict, ip_history

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"The file at {file_path} does not exist.")

    with open(file_path, 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            # pprint(line)

            ip_line = line.split()

            # 过滤空行及无备注的行
            if len(ip_line) <= 1:
                line = f.readline()
                continue
            ip_tmp = tuple(ip_line)
            k, v = ip_tmp[0], ip_tmp[1:]

            if not is_ipv4(k):
                print("Warning: no ipv4: ", end='')
                pprint(k)
                line = f.readline()
                continue

            if enable_tag:
                if k in ip_tag:
                    for i in v:
                        ip_tag[k].add(i)
                else:
                    ip_tag.update({k: set(v)})
                line = f.readline()
                continue

            if k in ip_dict:
                if v != ip_dict[k]:
                    # pprint(ip_dict[k])
                    old_ip = ip_dict.pop(k)
                    ip_dict.update({k: v})
                    ip_history.add((k,) + old_ip)
            else:
                ip_dict.update({k: v})

            # pprint(line.split())
            line = f.readline()


def clean_ip_history():
    """删历史IP"""
    history_ip = '192.168.1.1'
    list_to_remove = []
    for item in ip_history:
        if item[0] == history_ip:
            list_to_remove.append(item)

    for item in list_to_remove:
        ip_history.discard(item)


def regex(pattern, line):
    """匹配正则表达式"""
    match = pattern.findall(line)
    if not match:
        return
    return match


def regex_pos(pattern, line):
    """返回匹配的IP位置"""
    match = pattern.search(line)
    if not match:
        return len(line)
    return match.end()


def search_ip_dict(s):
    if s in ip_dict:
        return s + ' [' + ' '.join(ip_dict[s]) + ']'
    else:
        return s


def replace_ip():
    """替换字符串中的IP为带备注的版本"""
    pattern_ip = re.compile(
        r'((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))')
    f = sys.stdin
    line = f.readline()
    while line:
        ret = regex(pattern_ip, line)
        if ret:
            line_list = []
            for i in ret:
                ip1 = search_ip_dict(i)

                ip_end = regex_pos(pattern_ip, line)
                line_changed = line[0:ip_end]

                line_list.append(line_changed.replace(i, ip1))
                line = line[ip_end:]
            line_list.append(line)
            print(''.join(line_list), end='', flush=True)
            try:
                line = f.readline()
            except:
                pass
        else:
            print(line, end='', flush=True)
            try:
                line = f.readline()
            except:
                pass


def show():
    """显示 IP 字典内容"""

    print('IP dict:')
    print('-' * 30)

    if not ip_dict:
        print('(empty)')
    else:
        foreach_dict(ip_dict)

    print()
    print('IP history set:')
    print('=' * 30)

    if not ip_history:
        print('(empty)')
    else:
        foreach_set(ip_history)


def sort_ip_dict():
    """ ip 排序 """
    ip_obj = list()
    for key, value in ip_dict.items():
        # 将IP地址字符串转换为ipaddress.IPv4Address对象
        ip_obj.append(ipaddress.IPv4Address(key))

    # 对IP地址对象列表进行排序
    sorted_ips = sorted(ip_obj)

    # 打印排序后的IP地址
    for i in sorted_ips:
        ip = str(i)
        note = ' '.join(ip_dict[ip])

        # ipv4 最宽15个字符
        ip = ip.ljust(15, ' ')
        print(f'{ip}    {note}')


def sort_ip_history():
    """对历史IP数据排序并打印"""
    ip_his_list = list(ip_history)
    # pprint(ip_his_list)

    # 对IP地址对象列表进行排序
    sorted_ips = sorted(ip_his_list, key=lambda x: ipaddress.IPv4Address(x[0]))

    # pprint(sorted_ips)

    # 打印排序后的IP地址
    for i in sorted_ips:
        ip = i[0]
        note = ' '.join(i[1:])

        # ipv4 最宽15个字符
        ip = ip.ljust(15, ' ')
        print(f'{ip}    {note}')

def sort_ip_tag():
    """ ip 排序 """
    ip_obj = list()
    for key, value in ip_tag.items():
        # 将IP地址字符串转换为ipaddress.IPv4Address对象
        ip_obj.append(ipaddress.IPv4Address(key))

    # 对IP地址对象列表进行排序
    sorted_ips = sorted(ip_obj)

    # 打印排序后的IP地址
    for i in sorted_ips:
        ip = str(i)
        # tags = ' '.join(ip_tag[ip])

        # ipv4 最宽15个字符
        formatted_ip = ip.ljust(15, ' ')
        for tag in ip_tag[ip]:
            print(f'{formatted_ip}    {tag}')


def dump_ip_current():
    """导出IP 备注信息"""
    sort_ip_dict()
    sort_ip_history()


def erase(data_file_path):
    """重置数据文件"""
    global ip_dict, ip_history, ip_tag
    while True:
        user_input = input("请确认操作 (yes/no): ").lower()  # 将输入转换为小写，以便不区分大小写
        if user_input == 'yes':
            ip_dict = dict()
            ip_history = set()
            ip_tag = dict()
            save_data(data_file_path)
            break
        elif user_input == 'no':
            print("取消操作。")
            break
        else:
            print("无效的输入，请输入 'yes' 或 'no'。")


def search_arg(ip):
    """在字典中搜索IP并打印"""
    for key, value in ip_dict.items():
        if ip in key:
            formatted_key = key.ljust(15, ' ')
            note = ' '.join(value)
            print(f'{formatted_key}    {note}')


def change_default_encoding():
    """判断是否在 windows git-bash 下运行，是则使用 utf-8 编码"""
    if platform.system() == 'Windows':
        terminal = os.environ.get('TERM')
        if terminal and 'xterm' in terminal:
            sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def summary(enable_tag=False):
    """统计IP分类"""
    global ip_dict, ip_tag, tags
    if not enable_tag:
        for key, value in ip_dict.items():
            for tag in value:
                if tag in tags.keys():
                    tags[tag].append(key)
                else:
                    tags.update({tag: [key]})
    else:
        for key, value in ip_tag.items():
            for tag in value:
                if tag in tags.keys():
                    tags[tag].append(key)
                else:
                    tags.update({tag: [key]})

    sorted_items = sorted(tags.items(), key=lambda x: len(x[1]), reverse=True)
    for key, value in sorted_items:
        max_length = 15
        if len(key) > max_length:
            truncated_s = key[:max_length - 3] + "..."
        else:
            truncated_s = key
        print("{}  {}".format(align_text(truncated_s, 30), len(value)))


def align_text(text, width):
    """中文对齐"""
    text_width = wcwidth.wcswidth(text)
    if text_width < width:
        return text + ' ' * (width - text_width)
    else:
        return text


if __name__ == '__main__':

    # 如果是在 win git-bash 下运行，则使用 utf-8 编码替换标准输出默认编码
    change_default_encoding()

    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='IP 备注', formatter_class=argparse.RawTextHelpFormatter)

    # 添加命令行参数
    parser.add_argument('--ip_file', '-i', type=str, default='', help='IP 文件路径，文件内容格式：IP 备注')
    parser.add_argument('--data_file', '-d', type=str, default='IP.pkl',
                        help='数据文件路径\n默认数据文件查找顺序: \n  ./IP.pkl\n  ~/.ip_notes/IP.pkl\n')
    parser.add_argument('--interactive', '-a', action='store_true', help='读取管道中的内容，并进行IP替换')
    parser.add_argument('--list', '-l', action='store_true', help='显示IP字典中的内容')
    parser.add_argument('--erase', '-e', action='store_true', help='清空数据文件内容')
    parser.add_argument('--output_dict', '-od', action='store_true', help='输出IP字典信息')
    parser.add_argument('--output_history', '-oh', action='store_true', help='输出IP历史数据')
    parser.add_argument('--output_tag', '-ot', action='store_true', help='输出IP标签信息')
    parser.add_argument('--search', '-s', type=str, default='', help='在字典中搜索IP')
    parser.add_argument('--summary', '-m', action='store_true', help='统计 IP 分类')
    parser.add_argument('--tag', '-t', action='store_true', help='将 IP文件 当作标签数据处理')
    parser.add_argument('--debug', '-G', action='store_true', help='通过交互模式进行调试')
    parser.add_argument('--version', '-v', action='store_true', help='显示版本信息')

    # 解析命令行参数
    args = parser.parse_args()

    # 检查是否有传递任何参数，同时检查是否使用了默认参数
    if not any(vars(args).values()) or all(arg == parser.get_default(name) for name, arg in vars(args).items()):
        # 如果没有传递参数或者使用了默认参数，打印帮助信息
        parser.print_help()

    ip_file = args.ip_file
    data_file = args.data_file
    interactive = args.interactive
    show_ip = args.list
    erase_data = args.erase
    enable_output_dict = args.output_dict
    enable_output_history = args.output_history
    search_text = args.search
    enable_summary = args.summary
    enable_tag = args.tag
    enable_output_tag = args.output_tag

    if data_file == parser.get_default('data_file'):
        data_file = default_ipdata()
    # 反序列化，加载数据到字典
    load_data(data_file)

    # 从文本文件中装载数据
    if os.path.exists(ip_file):
        insert_ip_note(ip_file, enable_tag=enable_tag)

    # 从管道中读文件，替换IP为备注
    if interactive:
        replace_ip()

    # 显示IP字典
    if show_ip:
        show()

    # 重置数据文件
    if erase_data:
        erase(data_file)

    # 输出 IP 字典数据
    if enable_output_dict:
        sort_ip_dict()

    # 输出 IP 历史数据
    if enable_output_history:
        sort_ip_history()

    if enable_output_tag:
        sort_ip_tag()

    if search_text:
        search_arg(search_text)

    if enable_summary:
        summary(enable_tag=enable_tag)

    # 如果有文件输入，则存盘
    if ip_file:
        save_data(data_file)

    if args.version:
        print(f'ip_notes {version}')

    if args.debug:
        code.interact(local=locals())
