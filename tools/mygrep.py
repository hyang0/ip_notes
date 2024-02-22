import argparse
import re
import sys
import platform
import os

def change_default_encoding():
    '''判断是否在 windows git-bash 下运行，是则使用 utf-8 编码'''
    if platform.system() == 'Windows':
        terminal = os.environ.get('TERM')
        if terminal and 'xterm' in terminal:
            sys.stdin.reconfigure(encoding='utf-8')
            sys.stdout.reconfigure(encoding='utf-8')

def grep(pattern, file, use_regex):
    """
    类似于grep的函数，对每一行文本进行匹配，如果匹配则打印相应行，否则跳过。

    参数：
    pattern (str): 搜索模式，可以是正则表达式或子串
    file: 文件对象或标准输入
    use_regex (bool): 是否使用正则表达式匹配

    返回：
    None
    """
    for line in file:
        if use_regex:
            # 如果使用正则表达式匹配，使用re.search
            match = re.search(pattern, line)
        else:
            # 否则，使用普通的字符串查找
            match = pattern in line

        # 如果匹配成功，打印相应行
        if match:
            print(line, end='')

def main():
    change_default_encoding()
    # 创建命令行解析器
    parser = argparse.ArgumentParser(description="类似于grep的命令行工具，按行进行匹配。")

    # 添加命令行参数
    parser.add_argument("-e", "--regex", action="store_true",
                        help="使用正则表达式进行匹配")
    parser.add_argument("pattern", help="搜索模式，可以是正则表达式或子串")
    parser.add_argument("file", nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help="要搜索的文件，如果未提供则从标准输入读取")

    # 解析命令行参数
    args = parser.parse_args()

    try:
        # 调用grep函数，逐行处理文本
        grep(args.pattern, args.file, args.regex)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
