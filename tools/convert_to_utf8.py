import argparse
import chardet
import sys

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']

def convert_file_encoding(input_file_path, output_file_path):
    # 检测输入文件的编码
    input_encoding = detect_file_encoding(input_file_path)

    if not input_encoding:
        print("无法确定输入文件编码")
        return

    # 打开输入文件，并以检测到的编码读取内容
    with open(input_file_path, 'r', encoding=input_encoding) as input_file:
        content = input_file.read()

        # 打开输出文件或使用标准输出
        if output_file_path:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(content)
        else:
            sys.stdout.write(content)

def main():
    parser = argparse.ArgumentParser(description='Convert file encoding to UTF-8')
    parser.add_argument('-i', '--input', help='Input file path. If not provided, read from standard input.')
    parser.add_argument('-o', '--output', help='Output file path. If not provided, write to standard output.')

    args = parser.parse_args()

    if args.input:
        convert_file_encoding(args.input, args.output)
        print(f"文件已转换: {args.input} -> {args.output if args.output else '标准输出'}")
    else:
        # 从标准输入读取内容
        input_content = sys.stdin.read()

        # 如果提供了输出文件路径，则写入文件，否则写入标准输出
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as output_file:
                output_file.write(input_content)
            print(f"文件已转换: 标准输入 -> {args.output}")
        else:
            sys.stdout.write(input_content)

if __name__ == "__main__":
    main()
