#!/usr/bin/python3

import sys
import json

# Describes "namespace App\Http\Controllers\AnyFolder;"
def stmtNamespace(name, stmts):
    # Create a node for the "Stmt_Namespace" using "name"
    print('Stmt_Namespace -> {}'.format('\\'.join(name)))

    # Iterate through "stmt"s and connect "Stmt_Class" as a child
    # to the above parent namespace
    for node in stmts:
        if node['nodeType'] == 'Stmt_Class':
            stmtClass(node)
        elif node['nodeType'] == 'Stmt_Use':
            # In theory last array object should be the class declaration as it how syntax is arranged
            print('  {} USES {}'.format(stmts[-1]['name']['name'], '\\'.join(node['uses'][0]['name']['parts'])))

    # Iterate through "stmt"s and connect "Stmt_Use" for the above "Stmt_Class" node

# Describes "class ClassName extends AnotherClass"
def stmtClass(node):
    if node['name']['nodeType'] == 'Identifier':
        # Create the class node
        print('  Stmt_Class -> {}'.format(node['name']['name']))

    # If class contains "extends" or "implements", do that accordingly
    if node['extends']:
        # Create extended node for the class
        print('  {} EXTENDS {}'.format(node['name']['name'], ''.join(node['extends']['parts'])))

    if node['implements']:
        # Create implemented node for the class
        print('Implemented')

# Read the given array object from iterateSlices()
def readObject(slice):
    # Iterate through each key in current object
    for key in slice.keys():
        if key == 'nodeType':
            # nodeType: "Stmt_Namespace"
            if slice[key] == 'Stmt_Namespace':
                # Making sure [nodeType: "Name"] inside "name"
                if slice['name']['nodeType'] == 'Name':
                    stmtNamespace(slice['name']['parts'], slice['stmts'])
        else:
            print('[test] KEY: {}'.format(key))
            
        if type(slice[key]) is dict:
            print('[test] SUB KEYS: {}'.format(slice[key].keys()))

# Iterate through each json array object
def iterateObjects(currentFileJson):
    # slice eaquals to each object in json
    for slice in currentFileJson:
        readObject(slice)
        print('-----------------------------------')

# Opens the given file and return a json
def openFile(filePath):
    try:
        currentFile = open(filePath, 'r')
    except FileNotFoundError:
        print('File not found -> "{}"'.format(filePath))
        sys.exit(1)

    return json.loads(currentFile.read())

def main():
    fileDir = 'test-STs/samples-02/'
    filePath = fileDir+'ShodanNotificationController-ast.json'

    # Read json array objects
    iterateObjects(openFile(filePath))

if __name__ == '__main__':
    main()