#!/usr/bin/env python3

import argparse
import pyperclip


parser = argparse.ArgumentParser(description='''Copy a file to the clipboard''')
parser.add_argument('file', type=argparse.FileType('r'), help='file to copy')

args = parser.parse_args()

try:
    content = args.file.read()
    pyperclip.copy(content)

except UnicodeDecodeError:
    print('[-] Targeted file contains invalid Unicode sequences.')
    print('[-] Notice that copying binary files is not supported.')
