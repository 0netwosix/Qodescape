#!/usr/bin/python3

import argparse
import os
import sys
import time
from utils.support import Print

# Generate graph from AST
def generate_graph(file_path):
    command = 'python3 main.py {file_path}'.format(file_path=file_path)

    Print.info_print('[INFO]', 'Command running: {command}'.format(command=command))
    os.system(command)
    print('\n')

# Read a given directory
def read_dir(directory):
    file_list = os.listdir(directory)

    # Go through each file inside the directory
    for file in file_list:
        full_path = os.path.join(directory, file)

        # If it is a sub directory
        if os.path.isdir(full_path):
            read_dir(full_path)
        else:
            # If it is a json file
            if file.split('.')[-1] == 'json':
                generate_graph(full_path)

def init_argparse():
    parser = argparse.ArgumentParser(description='Parse PHP Abstract Syntax Tree (AST) into a Neo4j Graph.')
    parser.add_argument('path', help='path to AST (file-ast.json) file OR to directory')
    parser.add_argument('-f', '--file', action='store_true', help='a file path is given')
    parser.add_argument('-d', '--dir', action='store_true', help='a directory path is given')
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    duration = 0

    path = args.path

    if not (args.file and args.dir):
        if args.file:
            if os.path.isfile(path):
                start = time.time()
                generate_graph(path)
                end = time.time()
                duration = end - start
            else:
                Print.error_print('[FAIL]', 'Not a file: {path}'.format(path=path))
                sys.exit(1)
        elif args.dir:
            if os.path.isdir(path):
                start = time.time()
                read_dir(path)
                end = time.time()
                duration = end - start
            else:
                Print.error_print('[FAIL]', 'Not a directory: {path}'.format(path=path))
                sys.exit(1)
        else:
            Print.error_print('[FAIL]', 'Check optional arguments')
            sys.exit(1)
    else:
        Print.error_print('[FAIL]', 'Check optional arguments')
        sys.exit(1)

    Print.time_print(' Time taken: {duration}s '.format(duration=round(duration, 3)))

if __name__ == '__main__':
    main()