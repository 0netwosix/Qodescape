from utils import Print

'''
    Describes a namespace statement.
    Filename or Namespace would be the root node for each file. 

    TODO:
        1.) Re-evaluate logic and transfer "CLASS" node creation to "stmt_class()" if possible.
        2.) Create a seperate method to handle "Stmt_Use" nodeType. (look at 2.2 below)

    e.g.1. namespace App\Http\Controllers\AnyFolder ... class Scan {};
    e.g.2. use App\Models\Folder\File;

    HOW IT WORKS!
    1.) It creates "App\Http\Controllers\AnyFolder" node with following labels if it is not there already.
        - NAMESPACE
    2.) Then it looks at stmts inside namespace block and,
        2.1.) Calls "stmt_class()" to establish "CLASS" type node and the relationship.
        2.2.) Then it looks at the "Stmt_Use" staments,
            2.2.1.) It creates "File" node with following labels if it is not there already.
                - CLASS
            2.2.2.) It creates "App\Models\Folder" node with following labels if it is not there already.
                - NAMESPACE
            2.2.3.) Then it creats the following relationship if it does not exist already.
                - ("App\Models\Folder":{NAMESPACE})-[CONTAINS]->(File:{CLASS})
        2.3.) Once done it creats the following relationship if it does not exist already.
            - relationship_types = USES
            - (Scan:{CLASS})-[USES]->(File:{CLASS})
'''
def stmt_namespace(self, name, stmts):
    namespace_name = '\\'.join(name)
    # Create 'NAMESAPCE' node
    if not self.graph.find_node(namespace_name, 'NAMESPACE'):
        self.graph.create_node(namespace_name, 'NAMESPACE')

    # Iterate through "stmt"s and connect "Stmt_Class" as a child
    # to the above parent namespace
    if stmts:
        # Create the "Class" node first if exist
        # In theory last array object should be the class declaration as it how syntax is arranged
        if stmts[-1]['nodeType'] == 'Stmt_Class':
            self.stmt_class(stmts[-1], namespace_name, 'NAMESPACE', 'CONTAINS', namespace_name)

            for node in stmts:
                if node['nodeType'] == 'Stmt_Class':
                    continue
                # Iterate through "stmt"s and connect "Stmt_Use" for the above "Stmt_Class" node
                elif node['nodeType'] == 'Stmt_Use':
                    # Create 'NAMESPACE' node for the 'USE' class
                    if not self.graph.find_node('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE'):
                        self.graph.create_node('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE')

                    # Create 'CLASS' node for 'USE' class
                    if not self.graph.find_node(node['uses'][0]['name']['parts'][-1], 'CLASS'):
                        self.graph.create_node(node['uses'][0]['name']['parts'][-1], 'CLASS') 

                    # Create 'Namespace CONTAINS Class' relationship 
                    if not self.graph.find_relationship('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE', node['uses'][0]['name']['parts'][-1], 'CLASS', 'CONTAINS'):
                        self.graph.create_relationship('\\'.join(node['uses'][0]['name']['parts'][:-1]), 'NAMESPACE', node['uses'][0]['name']['parts'][-1], 'CLASS', 'CONTAINS') 

                    # Create 'Class USES AnotherClass' relationship
                    if not self.graph.find_relationship(stmts[-1]['name']['name'], 'CLASS', node['uses'][0]['name']['parts'][-1], 'CLASS', 'USES'):
                        self.graph.create_relationship(stmts[-1]['name']['name'], 'CLASS', node['uses'][0]['name']['parts'][-1], 'CLASS', 'USES')

                else:
                    Print.error_print('[404]', 'Different "nodeType": {}'.format(node['nodeType']))
        else:
            Print.error_print('[404]', 'Last list element is not a "Class" node: {}'.format(stmts[-1]['nodeType']))
