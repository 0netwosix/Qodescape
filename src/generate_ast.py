#!/usr/bin/python3

import sys
import os
from utils.support import Print

# Run "php-parse" command and generate [FILENAME]-ast.json
def create_ast_file(file_path):
    ast_dir_path = '{base_path}/ast'.format(base_path='/'.join(file_path.split('/')[:-1]))
    output_file = '{ast_dir_path}/{base_file_name}-ast.json'.format(ast_dir_path=ast_dir_path, base_file_name=file_path.split('/')[-1].split('.php')[0])
    command = 'php-parse -j {current_file} > {output_file}'.format(current_file=file_path, output_file=output_file)
    
    # Check if it has a "ast" directory, if not create one
    if not os.path.isdir(ast_dir_path):
        # Create ast directory
        os.mkdir(ast_dir_path)
        Print.success_print('[PASS]', 'ast Directory created: {ast_dir_path}'.format(ast_dir_path=ast_dir_path))

    Print.info_print('[INFO]', 'Command running: {command}\n'.format(command=command))
    os.system(command)


def main():
    usage_message = 'Usage: ./generate_ast.py [file path]'
    if len(sys.argv) == 2:
        if sys.argv[1].lower() == '--help':
            print(usage_message)
            sys.exit(1)
        file_path = sys.argv[1]
    else:
        Print.error_print('[FAIL]', 'No input file given')
        print(usage_message)
        sys.exit(1)

    create_ast_file(file_path)

if __name__ == '__main__':
    main()