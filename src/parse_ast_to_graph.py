#!/usr/bin/python3

import argparse
import os
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
    parser.add_argument('dir', help='The directory containing AST (file-ast.json) files')
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()

    directory = args.dir

    read_dir(directory)

if __name__ == '__main__':
    main()