#!/usr/bin/python3

import argparse
import os
import sys
import time

from utils import Print

# Run "php-parse" command and generate [FILENAME]-ast.json
def generate_ast_file(file_path):
    ast_dir_path = '{base_path}/ast'.format(base_path='/'.join(file_path.split('/')[:-1]))
    output_file = '{ast_dir_path}/{base_file_name}-ast.json'.format(ast_dir_path=ast_dir_path, base_file_name=file_path.split('/')[-1].split('.php')[0])
    command = 'php-parse -j {current_file} > {output_file}'.format(current_file=file_path, output_file=output_file)
    
    # Check if it has a "ast" directory, if not create one
    if not os.path.isdir(ast_dir_path):
        # Create ast directory
        os.mkdir(ast_dir_path)
        Print.success_print('[PASS]', 'ast Directory created: {ast_dir_path}\n'.format(ast_dir_path=ast_dir_path))

    Print.info_print('[INFO]', 'Command running: {command}'.format(command=command))
    os.system(command)
    Print.clear_print('\n')

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
            # If it is a php file
            if file.split('.')[-1] == 'php':
                generate_ast_file(full_path)

def init_argparse():
    parser = argparse.ArgumentParser(description='Generate an Abstract Syntax Tree (AST) using PHP-Parser.')
    parser.add_argument('path', help='path to PHP file OR to directory')
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
                generate_ast_file(path)
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