#!/usr/bin/python3

import sys
import json

fileDir = 'test-STs/'
filePath = fileDir+'ast-low.json'

try:
    currentFile = open(filePath, 'r')
except FileNotFoundError:
    print('File not found! ({})'.format(filePath))
    sys.exit(1)

currentFileJson = json.loads(currentFile.read())

print(len(currentFileJson))
# for line in currentFileJson[0]:
#     print(line)