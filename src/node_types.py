#!/usr/bin/python3

from utils.support import Print

class NodeType:
    def __init__(self, graph):
        self.graph = graph

    # Create a node for the FileName
    def filename_node(self, file_name):
        print('File_Name Node -> {file_name}'.format(file_name=file_name))

        # Create 'FILENAME' node
        if not self.graph.find_node(file_name, 'FILENAME'):
            self.graph.create_node(file_name, 'FILENAME')
        else:
            Print.errorPrint('Node exist: ', '{node_name} {node_type}'.format(
                node_name=file_name, 
                node_type='FILENAME'))

    # Describes "namespace App\Http\Controllers\AnyFolder;"
    def stmt_namespace(self, name, stmts):
        namespace_name = '\\'.join(name)
        # Create a node for the "Stmt_Namespace" using "name"
        print('Stmt_Namespace -> {namespace_name}'.format(namespace_name=namespace_name))

        # Create 'NAMESAPCE' node
        if not self.graph.find_node(namespace_name, 'NAMESPACE'):
            self.graph.create_node(namespace_name, 'NAMESPACE')
        else:
            Print.errorPrint('Node exist: ', '{node_name} {node_type}'.format(
                node_name=namespace_name, 
                node_type='NAMESPACE'))

        # Iterate through "stmt"s and connect "Stmt_Class" as a child
        # to the above parent namespace
        if stmts:
            # Create the "Class" node first if exist
            # In theory last array object should be the class declaration as it how syntax is arranged
            if stmts[-1]['nodeType'] == 'Stmt_Class':
                self.stmt_class(stmts[-1], namespace_name, 'NAMESPACE', 'CONTAINS')

                for node in stmts:
                    if node['nodeType'] == 'Stmt_Class':
                        continue
                    # Iterate through "stmt"s and connect "Stmt_Use" for the above "Stmt_Class" node
                    elif node['nodeType'] == 'Stmt_Use':
                        print('{class_name} USES {use_path} {use_class_name}'.format(
                            class_name=stmts[-1]['name']['name'], 
                            use_path='\\'.join(node['uses'][0]['name']['parts'][:-1]), 
                            use_class_name=node['uses'][0]['name']['parts'][-1]
                        ))

                        # Create 'NAMESPACE' node
                        if not self.graph.find_node('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE'):
                            self.graph.create_node('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE')
                        else:
                            Print.errorPrint('Node exist: ', '{node_name} {node_type}'.format(
                                node_name='\\'.join(node['uses'][0]['name']['parts'][:-1]), 
                                node_type='NAMESPACE'
                            ))

                        # Create 'CLASS' node
                        if not self.graph.find_node(node['uses'][0]['name']['parts'][-1], 'CLASS'):
                            self.graph.create_node(node['uses'][0]['name']['parts'][-1], 'CLASS')
                        else:
                            Print.errorPrint('Node exist: ', '{node_name} {node_type}'.format(
                                node_name=node['uses'][0]['name']['parts'][-1],
                                node_type='CLASS'
                            ))   

                        # Create 'Namespace CONTAINS Class' relationship 
                        if not self.graph.find_relationship('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE', node['uses'][0]['name']['parts'][-1], 'CLASS', 'CONTAINS'):
                            self.graph.create_relationship('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE', node['uses'][0]['name']['parts'][-1], 'CLASS', 'CONTAINS') 
                        else:
                            Print.errorPrint('Relationship exist: ', '{parent_node} {relationship_type} {child_node}'.format(
                                parent_node='\\'.join(node['uses'][0]['name']['parts'][:-1]),
                                relationship_type='CONTAINS',
                                child_node=node['uses'][0]['name']['parts'][-1]
                            ))

                        # Create 'Class USES AnotherClass' relationship
                        if not self.graph.find_relationship(stmts[-1]['name']['name'], 'CLASS', node['uses'][0]['name']['parts'][-1], 'CLASS', 'USES'):
                            self.graph.create_relationship(stmts[-1]['name']['name'], 'CLASS', node['uses'][0]['name']['parts'][-1], 'CLASS', 'USES')
                        else:
                            Print.errorPrint('Relationship exist: ', '{parent_node} {relationship_type} {child_node}'.format(
                                parent_node=stmts[-1]['name']['name'],
                                relationship_type='USES',
                                child_node=node['uses'][0]['name']['parts'][-1]
                            ))

                    else:
                        Print.errorPrint('Different "nodeType": ', '{}'.format(node['nodeType']))
            else:
                Print.errorPrint('Last list element is not a "Class" node: ', '{}'.format(stmts[-1]['nodeType']))

    # Describes "class ClassName extends AnotherClass implements SomeOtherClass"
    def stmt_class(self, node, parent_node=None, parent_node_type=None, relationship_type=None):
        if node['name']['nodeType'] == 'Identifier':
            # Create the class node
            print('Stmt_Class -> {}'.format(node['name']['name']))

            # Create 'CLASS' node
            if not self.graph.find_node(node['name']['name'], 'CLASS'):
                self.graph.create_node(node['name']['name'], 'CLASS')
            else:
                Print.errorPrint('Node exist: ', '{node_name} {node_type}'.format(
                    node_name=node['name']['name'],
                    node_type='CLASS'
                ))

            # Create 'Namespace CONTAINS Class' relationship
            if not self.graph.find_relationship(parent_node, parent_node_type, node['name']['name'], 'CLASS', relationship_type):
                self.graph.create_relationship(parent_node, parent_node_type, node['name']['name'], 'CLASS', relationship_type)
            else:
                Print.errorPrint('Relationship exist: ', '{parent_node} {relationship_type} {child_node}'.format(
                    parent_node=parent_node,
                    relationship_type=relationship_type,
                    child_node=node['name']['name']
                ))    

        # If class contains "extends"
        if node['extends']:
            # Create extended node for the class
            print('{this_node} EXTENDS {extened_node}'.format(
                this_node=node['name']['name'], 
                extened_node='\\'.join(node['extends']['parts'])
            ))

            # Create extended 'CLASS' node
            if not self.graph.find_node('\\'.join(node['extends']['parts']), 'CLASS'):
                self.graph.create_node('\\'.join(node['extends']['parts']), 'CLASS')
            else:
                Print.errorPrint('Node exist: ', '{node_name} {node_type}'.format(
                    node_name='\\'.join(node['extends']['parts']),
                    node_type='CLASS'
                ))

            # Create 'Class EXTENDS AnotherClass' relationship
            if not self.graph.find_relationship(node['name']['name'], 'CLASS', '\\'.join(node['extends']['parts']), 'CLASS', 'EXTENDS'):
                self.graph.create_relationship(node['name']['name'], 'CLASS', '\\'.join(node['extends']['parts']), 'CLASS', 'EXTENDS')
            else:
                Print.errorPrint('Relationship exist: ', '{parent_node} {relationship_type} {child_node}'.format(
                    parent_node=node['name']['name'],
                    relationship_type='EXTENDS',
                    child_node='\\'.join(node['extends']['parts'])
                ))    

        # If class contains "implements"
        if node['implements']:
            for interface in node['implements']:
                # Create each implemented node for the class
                print('{this_node} IMPLEMENTS {implemented_node}'.format(
                    this_node=node['name']['name'],
                    implemented_node='\\'.join(interface['parts'])
                ))

                # Create implemented 'CLASS' node
                if not self.graph.find_node('\\'.join(interface['parts']), 'CLASS'):
                    self.graph.create_node('\\'.join(interface['parts']), 'CLASS')
                else:
                    Print.errorPrint('Node exist: ', '{node_name} {node_type}'.format(
                        node_name='\\'.join(interface['parts']),
                        node_type='CLASS'
                    ))  

                # Create 'Class IMPLEMENTS AnotherClass' relationship
                if not self.graph.find_relationship(node['name']['name'], 'CLASS', '\\'.join(interface['parts']), 'CLASS', 'IMPLEMENTS'):
                    self.graph.create_relationship(node['name']['name'], 'CLASS', '\\'.join(interface['parts']), 'CLASS', 'IMPLEMENTS')
                else:
                    Print.errorPrint('Relationship exist: ', '{parent_node} {relationship_type} {child_node}'.format(
                        parent_node=node['name']['name'],
                        relationship_type='IMPLEMENTS',
                        child_node='\\'.join(interface['parts'])
                    ))              
