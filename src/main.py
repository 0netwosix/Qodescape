#!/usr/bin/python3

import sys
import json
from termcolor import colored
from graph import Graph

# Red text
def errorPrint(colored_message, message=None):
    print("{colored_message} {message}".format(
        colored_message=colored(colored_message, 'red'),
        message=message
    ))

# Describes "namespace App\Http\Controllers\AnyFolder;"
def stmtNamespace(name, stmts):
    namespaceName = '\\'.join(name)
    # Create a node for the "Stmt_Namespace" using "name"
    print('Stmt_Namespace -> {namespaceName}'.format(namespaceName=namespaceName))

    # Create 'NAMESAPCE' node
    if not graph.find_node(namespaceName, 'NAMESPACE'):
        graph.create_node(namespaceName, 'NAMESPACE')
    else:
        errorPrint('Node exist: ', '{nodeName} {nodeType}'.format(nodeName=namespaceName, nodeType='NAMESPACE'))

    # Iterate through "stmt"s and connect "Stmt_Class" as a child
    # to the above parent namespace
    if stmts:
        # Create the "Class" node first if exist
        # In theory last array object should be the class declaration as it how syntax is arranged
        if stmts[-1]['nodeType'] == 'Stmt_Class':
            stmtClass(stmts[-1], namespaceName, 'NAMESPACE', 'CONTAINS')

            for node in stmts:
                if node['nodeType'] == 'Stmt_Class':
                    continue
                # Iterate through "stmt"s and connect "Stmt_Use" for the above "Stmt_Class" node
                elif node['nodeType'] == 'Stmt_Use':
                    print('{className} USES {usePath} {useClassName}'.format(
                        className=stmts[-1]['name']['name'], 
                        usePath='\\'.join(node['uses'][0]['name']['parts'][:-1]), 
                        useClassName=node['uses'][0]['name']['parts'][-1]
                    ))

                    # Create 'NAMESPACE' node
                    if not graph.find_node('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE'):
                        graph.create_node('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE')
                    else:
                        errorPrint('Node exist: ', '{nodeName} {nodeType}'.format(
                            nodeName='\\'.join(node['uses'][0]['name']['parts'][:-1]), 
                            nodeType='NAMESPACE'
                        ))

                    # Create 'CLASS' node
                    if not graph.find_node(node['uses'][0]['name']['parts'][-1], 'CLASS'):
                        graph.create_node(node['uses'][0]['name']['parts'][-1], 'CLASS')
                    else:
                        errorPrint('Node exist: ', '{nodeName} {nodeType}'.format(
                            nodeName=node['uses'][0]['name']['parts'][-1],
                            nodeType='CLASS'
                        ))   

                    # Create 'Namespace CONTAINS Class' relationship 
                    if not graph.find_relationship('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE', node['uses'][0]['name']['parts'][-1], 'CLASS', 'CONTAINS'):
                        graph.create_relationship('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE', node['uses'][0]['name']['parts'][-1], 'CLASS', 'CONTAINS') 
                    else:
                        errorPrint('Relationship exist: ', '{parentNode} {relationshipType} {childNode}'.format(
                            parentNode='\\'.join(node['uses'][0]['name']['parts'][:-1]),
                            relationshipType='CONTAINS',
                            childNode=node['uses'][0]['name']['parts'][-1]
                        ))

                    # Create 'Class USES AnotherClass' relationship
                    if not graph.find_relationship(stmts[-1]['name']['name'], 'CLASS', node['uses'][0]['name']['parts'][-1], 'CLASS', 'USES'):
                        graph.create_relationship(stmts[-1]['name']['name'], 'CLASS', node['uses'][0]['name']['parts'][-1], 'CLASS', 'USES')
                    else:
                        errorPrint('Relationship exist: ', '{parentNode} {relationshipType} {childNode}'.format(
                            parentNode=stmts[-1]['name']['name'],
                            relationshipType='USES',
                            childNode=node['uses'][0]['name']['parts'][-1]
                        ))

                else:
                    errorPrint('Different "nodeType": ', '{}'.format(node['nodeType']))
        else:
            errorPrint('Last list element is not a "Class" node: ', '{}'.format(stmts[-1]['nodeType']))

# Describes "class ClassName extends AnotherClass implements SomeOtherClass"
def stmtClass(node, parentNode=None, parentNodeType=None, relationshipType=None):
    if node['name']['nodeType'] == 'Identifier':
        # Create the class node
        print('Stmt_Class -> {}'.format(node['name']['name']))

        # Create 'CLASS' node
        if not graph.find_node(node['name']['name'], 'CLASS'):
            graph.create_node(node['name']['name'], 'CLASS')
        else:
            errorPrint('Node exist: ', '{nodeName} {nodeType}'.format(
                nodeName=node['name']['name'],
                nodeType='CLASS'
            ))

        # Create 'Namespace CONTAINS Class' relationship
        if not graph.find_relationship(parentNode, parentNodeType, node['name']['name'], 'CLASS', relationshipType):
            graph.create_relationship(parentNode, parentNodeType, node['name']['name'], 'CLASS', relationshipType)
        else:
            errorPrint('Relationship exist: ', '{parentNode} {relationshipType} {childNode}'.format(
                parentNode=parentNode,
                relationshipType=relationshipType,
                childNode=node['name']['name']
            ))    

    # If class contains "extends"
    if node['extends']:
        # Create extended node for the class
        print('{thisNode} EXTENDS {extendedNode}'.format(
            thisNode=node['name']['name'], 
            extendedNode='\\'.join(node['extends']['parts'])
        ))

        # Create extended 'CLASS' node
        if not graph.find_node('\\'.join(node['extends']['parts']), 'CLASS'):
            graph.create_node('\\'.join(node['extends']['parts']), 'CLASS')
        else:
            errorPrint('Node exist: ', '{nodeName} {nodeType}'.format(
                nodeName='\\'.join(node['extends']['parts']),
                nodeType='CLASS'
            ))

        # Create 'Class EXTENDS AnotherClass' relationship
        if not graph.find_relationship(node['name']['name'], 'CLASS', '\\'.join(node['extends']['parts']), 'CLASS', 'EXTENDS'):
            graph.create_relationship(node['name']['name'], 'CLASS', '\\'.join(node['extends']['parts']), 'CLASS', 'EXTENDS')
        else:
            errorPrint('Relationship exist: ', '{parentNode} {relationshipType} {childNode}'.format(
                parentNode=node['name']['name'],
                relationshipType='EXTENDS',
                childNode='\\'.join(node['extends']['parts'])
            ))    

    # If class contains "implements"
    if node['implements']:
        for interface in node['implements']:
            # Create each implemented node for the class
            print('{thisNode} IMPLEMENTS {implementedNode}'.format(
                thisNode=node['name']['name'],
                implementedNode='\\'.join(interface['parts'])
            ))

            # Create implemented 'CLASS' node
            if not graph.find_node('\\'.join(interface['parts']), 'CLASS'):
                graph.create_node('\\'.join(interface['parts']), 'CLASS')
            else:
                errorPrint('Node exist: ', '{nodeName} {nodeType}'.format(
                    nodeName='\\'.join(interface['parts']),
                    nodeType='CLASS'
                ))  

            # Create 'Class IMPLEMENTS AnotherClass' relationship
            if not graph.find_relationship(node['name']['name'], 'CLASS', '\\'.join(interface['parts']), 'CLASS', 'IMPLEMENTS'):
                graph.create_relationship(node['name']['name'], 'CLASS', '\\'.join(interface['parts']), 'CLASS', 'IMPLEMENTS')
            else:
                errorPrint('Relationship exist: ', '{parentNode} {relationshipType} {childNode}'.format(
                    parentNode=node['name']['name'],
                    relationshipType='IMPLEMENTS',
                    childNode='\\'.join(interface['parts'])
                ))              

# Read the given array object from iterateObjects()
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
        errorPrint('[ERROR] File not found: ', '{}'.format(filePath))
        sys.exit(1)

    return json.loads(currentFile.read())


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print('Usage: ./main.py [file path]')
            sys.exit(1)
        filePath = sys.argv[1]
    else:
        fileDir = '../test-STs/samples-02/'
        filePath = fileDir+'LaunchOnDemandScan-with-Shodan-ast.json'

    # Read json array objects
    iterateObjects(openFile(filePath))

if __name__ == '__main__':
    graph = Graph()
    main()
    graph.close()
