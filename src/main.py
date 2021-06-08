#!/usr/bin/python3

import sys
import json
from graph import Graph
from node_types import NodeType
from utils.support import Print

# Read the given array object from iterateObjects()
def read_object(slice):
    # Iterate through each key in current object
    for key in slice.keys():
        if key == 'nodeType':
            print('[test] KEY: {} -> {}'.format(key, slice[key]))

            # nodeType: "Stmt_InlineHTML"
            if slice[key] == 'Stmt_InlineHTML':
                continue

            # nodeType: "Stmt_Namespace"
            if slice[key] == 'Stmt_Namespace':
                # Making sure [nodeType: "Name"] inside "name"
                if slice['name']['nodeType'] == 'Name':
                    node_type.stmt_namespace(slice['name']['parts'], slice['stmts'])
            else:
                # Create a node for the FileName
                node_type.filename_node(file_name)
        else:
            print('[test] KEY: {}'.format(key))
            
            
            
        if type(slice[key]) is dict:
            print('[test] SUB KEYS: {}'.format(slice[key].keys()))

# Iterate through each json array object
def iterate_objects(current_file_json):
    # slice eaquals to each object in json
    for slice in current_file_json:
        read_object(slice)
        print('-----------------------------------')

# Opens the given file and return a json
def open_file(file_path):
    try:
        current_file = open(file_path, 'r')
    except FileNotFoundError:
        Print.errorPrint('[ERROR] File not found: ', '{}'.format(file_path))
        sys.exit(1)

    return json.loads(current_file.read())


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print('Usage: ./main.py [file path]')
            sys.exit(1)
        file_path = sys.argv[1]
    else:
        file_dir = '../test-STs/samples-02/'
        file_path = file_dir+'LaunchOnDemandScan-with-Shodan-ast.json'

    # To get filename if 'namespace' is not there
    global file_name
    file_name = '{}.php'.format(file_path.split('/')[-1].split('-ast.json')[0])

    # Read json array objects
    iterate_objects(open_file(file_path))

if __name__ == '__main__':
    graph = Graph()
    node_type = NodeType(graph)
    main()
    graph.close()
