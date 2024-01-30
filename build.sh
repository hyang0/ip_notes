#!/bin/bash

rm -rfv build
rm -rfv dist

pyinstaller --onefile --clean --ico ./img/IP.ico ip_notes.py
pyinstaller --onefile tools/check_file_encoding.py
pyinstaller --onefile tools/convert_to_utf8.py
pyinstaller --onefile tools/mygrep.py
