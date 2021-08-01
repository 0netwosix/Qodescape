from utils.support import Print

# Describes "namespace App\Http\Controllers\AnyFolder;"
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
                    Print.error_print('[ERROR]', 'Different "nodeType": {}'.format(node['nodeType']))
        else:
            Print.error_print('[ERROR]', 'Last list element is not a "Class" node: {}'.format(stmts[-1]['nodeType']))
