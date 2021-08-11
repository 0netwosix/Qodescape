#!/usr/bin/python3

import argparse
import json
import sys

import graph
import nodetypes
from utils import Print

# Read the given array object from iterateObjects()
def read_object(slice):
    # Iterate through each key in current object
    for key, value in slice.items():
        if key == 'nodeType':
            Print.clear_print('[main] KEY: {} -> {}'.format(key, value))

            # nodeType: "Stmt_InlineHTML"
            if value == 'Stmt_InlineHTML':
                continue

            # nodeType: "Stmt_Namespace"
            if value == 'Stmt_Namespace':
                # Making sure [nodeType: "Name"] inside "name"
                if slice['name']['nodeType'] == 'Name':
                    node_type.stmt_namespace(slice['name']['parts'], slice['stmts'])
            else:
                # Create a node for the FileName
                node_type.filename_node(file_name)

                # If true, parent_node = file_name
                no_namespace = True

            if value == 'Stmt_Global':
                node_type.stmt_global(slice['vars'], file_name, 'FILENAME', file_name)
            elif value == 'Stmt_Class':
                node_type.stmt_class(slice, file_name, 'FILENAME', 'CONTAINS', file_name)
            elif value == 'Stmt_Expression':
                # Parent node is considered as 'file_name'
                node_type.stmt_expression(slice['expr'], file_name, 'FILENAME', file_name)
            elif value == 'Stmt_Echo':
                # Parent node is considered as 'file_name'
                node_type.stmt_echo(slice['exprs'], file_name, 'FILENAME', file_name)
            elif value == 'Stmt_If':
                node_type.stmt_if(slice, file_name, 'FILENAME', file_name)

        elif type(value) is dict:
            Print.clear_print('[main] DICT: {} -> {}'.format(key ,value.keys()))
        else:
            Print.clear_print('[main] KEY: {}'.format(key))
            

# Iterate through each json array object
def iterate_objects(current_file_json):
    # slice eaquals to each object in json
    for slice in current_file_json:
        read_object(slice)
        Print.clear_print('-----------------------------------')

# Opens the given file and return a json
def open_file(file_path):
    try:
        current_file = open(file_path, 'r')
    except FileNotFoundError:
        Print.error_print('[FAIL]', 'File not found: {}'.format(file_path))
        sys.exit(1)

    return json.loads(current_file.read())

def init_argparse():
    parser = argparse.ArgumentParser(description='Parse PHP Abstract Syntax Tree (AST) into a Neo4j Graph.')
    parser.add_argument('file', help='File you need to parse')
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()

    file_path = args.file

    # To get filename 
    global file_name
    file_name = file_path.split('/')[-1].split('-ast.json')[0]

    # If 'namespace' is not there, parent node should be above 'file_name'
    global no_namespace
    no_namespace = False

    # Read json array objects
    iterate_objects(open_file(file_path))

if __name__ == '__main__':
    graph = graph.Graph()
    node_type = nodetypes.NodeTypes(graph)
    main()
    graph.close()