import chardet
import argparse
import glob
import os

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

def check_file_encodings(files):
    for file_path in files:
        if is_file(file_path):
            encoding = detect_file_encoding(file_path)
            formatted_file_path = "{:<20}".format(file_path)
            print(f"{formatted_file_path}\t编码: {encoding if encoding else '无法确定'}")

def main():
    parser = argparse.ArgumentParser(description='Check file encodings')
    parser.add_argument('files', nargs='+', help='File paths to check. You can use * for wildcard expansion.')

    args = parser.parse_args()

    # 使用 glob 模块进行通配符扩展
    expanded_files = [file_path for pattern in args.files for file_path in glob.glob(pattern) if is_file(file_path)]
    
    check_file_encodings(expanded_files)

if __name__ == "__main__":
    main()
