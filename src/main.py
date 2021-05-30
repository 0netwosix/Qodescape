#!/usr/bin/python3

import sys
import json
from termcolor import cprint
from graph import Graph

# Red text
def errorPrint(message):
    cprint(message, 'red')

# Describes "namespace App\Http\Controllers\AnyFolder;"
def stmtNamespace(name, stmts):
    namespaceName = '\\'.join(name)
    # Create a node for the "Stmt_Namespace" using "name"
    print('Stmt_Namespace -> {namespaceName}'.format(namespaceName=namespaceName))

    # Create 'NAMESAPCE' node
    '''Check if a node exist with the given name'''
    graph.create_node(namespaceName, 'NAMESPACE')

    # Iterate through "stmt"s and connect "Stmt_Class" as a child
    # to the above parent namespace
    if stmts:
        # Create the "Class" node first if exist
        if stmts[-1]['nodeType'] == 'Stmt_Class':
            stmtClass(stmts[-1], namespaceName, 'NAMESPACE', 'CONTAINS')
        else:
            errorPrint('  Last list element is not a "Class" node: {}'.format(stmts[-1]['nodeType']))

        for node in stmts:
            if node['nodeType'] == 'Stmt_Class':
                continue
            elif node['nodeType'] == 'Stmt_Use':
                # In theory last array object should be the class declaration as it how syntax is arranged
                print('  {className} USES {useName}'.format(className=stmts[-1]['name']['name'], useName='\\'.join(node['uses'][0]['name']['parts'])))

                # Create 'CLASS' node
                '''Check if a node exist with the given name'''
                graph.create_node('\\'.join(node['uses'][0]['name']['parts']), 'CLASS')
                graph.create_relationship(stmts[-1]['name']['name'], 'CLASS', '\\'.join(node['uses'][0]['name']['parts']), 'CLASS', 'USES')

            else:
                errorPrint('  Different "nodeType": {}'.format(node['nodeType']))

    # Iterate through "stmt"s and connect "Stmt_Use" for the above "Stmt_Class" node

# Describes "class ClassName extends AnotherClass implements SomeOtherClass"
def stmtClass(node, parentNode=None, parentNodeType=None, relationshipType=None):
    if node['name']['nodeType'] == 'Identifier':
        # Create the class node
        print('  Stmt_Class -> {}'.format(node['name']['name']))

        # Create 'CLASS' node
        '''Check if a node exist with the given name'''
        graph.create_node(node['name']['name'], 'CLASS')
        graph.create_relationship(parentNode, parentNodeType, node['name']['name'], 'CLASS', relationshipType)

    # If class contains "extends" or "implements", do that accordingly
    if node['extends']:
        # Create extended node for the class
        print('  {} EXTENDS {}'.format(node['name']['name'], '\\'.join(node['extends']['parts'])))

        # Create 'CLASS' node
        '''Check if a node exist with the given name'''
        graph.create_node('\\'.join(node['extends']['parts']), 'CLASS')
        graph.create_relationship(node['name']['name'], 'CLASS', '\\'.join(node['extends']['parts']), 'CLASS', 'EXTENDS')

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
    fileDir = '../test-STs/samples-02/'
    filePath = fileDir+'ShodanNotificationController-ast.json'

    # Read json array objects
    iterateObjects(openFile(filePath))

if __name__ == '__main__':
    graph = Graph()
    main()
    graph.close()
