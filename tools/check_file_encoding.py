import chardet
import argparse
import glob
import os
import platform
import sys


def change_default_encoding():
    """判断是否在 windows git-bash 下运行，是则使用 utf-8 编码"""
    if platform.system() == 'Windows':
        terminal = os.environ.get('TERM')
        if terminal and 'xterm' in terminal:
            sys.stdin.reconfigure(encoding='utf-8')
            sys.stdout.reconfigure(encoding='utf-8')


def is_file(file_path):
    return os.path.isfile(file_path)


def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']


def check_crlf_ending(file_path):
    with open(file_path, 'rb') as file:
        line = file.read(1000)
        # print(repr(line))
        if b'\r\n' in line or b'\r\x00\n' in line:
            return 'CRLF'

        if b'\r' in line:
            return 'CR'

        return 'LF'


def check_file_encodings(files):
    for file_path in files:
        if is_file(file_path):
            encoding = detect_file_encoding(file_path)
            ending = check_crlf_ending(file_path)
            formatted_file_path = "{:<20}".format(file_path)
            print(
                f"{formatted_file_path}\t编码: {encoding if encoding else '无法确定'}\t换行: {ending if ending else '无法确定'}")


def main():
    parser = argparse.ArgumentParser(description='Check file encodings')
    parser.add_argument(
        'files', nargs='+', help='File paths to check. You can use * for wildcard expansion.')

    args = parser.parse_args()

    # 使用 glob 模块进行通配符扩展
    expanded_files = [file_path for pattern in args.files for file_path in glob.glob(
        pattern) if is_file(file_path)]

    check_file_encodings(expanded_files)


if __name__ == "__main__":
    change_default_encoding()
    main()
