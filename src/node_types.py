#!/usr/bin/python3

from utils.support import Print

class NodeType:
    def __init__(self, graph):
        self.graph = graph

    def stmt_expression(self, expr, parent_node, parent_node_type):
        if expr['nodeType'] == 'Expr_Assign':
            # Create the variable and its relationship with the parent node
            if expr['var']['nodeType'] == 'Expr_Variable':
                self.expr_variable(expr, parent_node, parent_node_type)

            ''' Following describes the value of above variable
            '''
            # If the value of above variable is a "String"
            if expr['expr']['nodeType'] == 'Scalar_String':
                # Need to decide
                pass
            # If the value of the above variable is a "Function call"
            elif expr['expr']['nodeType'] == 'Expr_FuncCall':
                self.expr_func_call(expr['expr'], expr['var']['name'], 'VARIABLE')
            # If the value of the above variable is similar to "$GET['id']"
            elif expr['expr']['nodeType'] == 'Expr_ArrayDimFetch':
                self.expr_array_dim_fetch(expr['expr'], expr['var']['name'], 'VARIABLE', 'ASSIGNS')
            # If the value of the above variable is similar to "select * from `products` where productCode='$prodCode'"
            elif expr['expr']['nodeType'] == 'Scalar_Encapsed':
                if expr['expr']['parts']:
                    # Loop through the parts of the string
                    for part in expr['expr']['parts']:
                        if part['nodeType'] == 'Expr_Variable':
                            # This variable must have a node at this point, if not something is not right
                            if self.graph.find_node(part['name'], 'VARIABLE'):
                                # If it has the node, create the relationship with the variable to which it refers
                                if not self.graph.find_relationship(expr['var']['name'], 'VARIABLE', part['name'], 'VARIABLE', 'ASSIGNS'):
                                    self.graph.create_relationship(expr['var']['name'], 'VARIABLE', part['name'], 'VARIABLE', 'ASSIGNS')
                            else:
                                Print.errorPrint('NOT FOUND ', '[NODE]: {}'.format(part['name']))


        elif expr['nodeType'] == 'Expr_FuncCall':
            self.expr_func_call(expr, parent_node, parent_node_type)

    def expr_array_dim_fetch(self, expr, parent_node, parent_node_type, relationship_type):
        # Create the node
        if not self.graph.find_node(expr['var']['name'], 'VARIABLE'):
            self.graph.create_node(expr['var']['name'], 'VARIABLE')

        # Create the relationship
        if not self.graph.find_relationship(parent_node, parent_node_type, expr['var']['name'], 'VARIABLE', relationship_type):
            self.graph.create_relationship(parent_node, parent_node_type, expr['var']['name'], 'VARIABLE', relationship_type)
                
    # Create a function call relationship in > "$result = mysqli_query($con, $query);"
    # It creates just the function call, not the function defineition node
    def expr_func_call(self, expr, parent_node, parent_node_type):
        # Create "FUNCTION_CALL" node
        if not self.graph.find_node(" ".join(expr['name']['parts']), 'FUNCTION_CALL'):
            self.graph.create_node(" ".join(expr['name']['parts']), 'FUNCTION_CALL')

        # Create "FUNCTION_CALL" relationship
        if not self.graph.find_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), 'FUNCTION_CALL', 'FUNCTION_CALL'):
            self.graph.create_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), 'FUNCTION_CALL', 'FUNCTION_CALL')

        if expr['args']:
            for argument in expr['args']:
                # If argument is a variable, else it should be scalar_string
                if 'name' in argument['value']:
                    # Create argument node if it is not there
                    if not self.graph.find_node(argument['value']['name'], 'VARIABLE'):
                        self.graph.create_node(argument['value']['name'], 'VARIABLE')

                    # Create the "IS_ARGUMENT" relationship
                    if not self.graph.find_relationship(" ".join(expr['name']['parts']), 'FUNCTION_CALL', argument['value']['name'], 'VARIABLE', 'IS_ARGUMENT'):
                        self.graph.create_relationship(" ".join(expr['name']['parts']), 'FUNCTION_CALL', argument['value']['name'], 'VARIABLE', 'IS_ARGUMENT')

    # Create a variable and its relationship
    def expr_variable(self, expr, parent_node, parent_node_type):
        # Create the variable implementing a relationship with the parent
        if not self.graph.find_node(expr['var']['name'], 'VARIABLE'):
            self.graph.create_node(expr['var']['name'], 'VARIABLE')

        # Create the relationship with the parent
        if not self.graph.find_relationship(parent_node, parent_node_type, expr['var']['name'], 'VARIABLE', 'IS_VARIABLE'):
            self.graph.create_relationship(parent_node, parent_node_type, expr['var']['name'], 'VARIABLE', 'IS_VARIABLE')

    # Create a node for the FileName
    def filename_node(self, file_name):
        # Create 'FILENAME' node
        if not self.graph.find_node(file_name, 'FILENAME'):
            # print('File_Name Node -> {file_name}'.format(file_name=file_name))
            self.graph.create_node(file_name, 'FILENAME')

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
                self.stmt_class(stmts[-1], namespace_name, 'NAMESPACE', 'CONTAINS')

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
                        Print.errorPrint('Different "nodeType": ', '{}'.format(node['nodeType']))
            else:
                Print.errorPrint('Last list element is not a "Class" node: ', '{}'.format(stmts[-1]['nodeType']))

    # Describes "class ClassName extends AnotherClass implements SomeOtherClass"
    def stmt_class(self, node, parent_node=None, parent_node_type=None, relationship_type=None):
        if node['name']['nodeType'] == 'Identifier':
            # Create 'CLASS' node
            if not self.graph.find_node(node['name']['name'], 'CLASS'):
                self.graph.create_node(node['name']['name'], 'CLASS')

            # Create 'Namespace CONTAINS Class' relationship
            if not self.graph.find_relationship(parent_node, parent_node_type, node['name']['name'], 'CLASS', relationship_type):
                self.graph.create_relationship(parent_node, parent_node_type, node['name']['name'], 'CLASS', relationship_type)  

        # If class contains "extends"
        if node['extends']:
            # Create extended 'CLASS' node
            if not self.graph.find_node('\\'.join(node['extends']['parts']), 'CLASS'):
                self.graph.create_node('\\'.join(node['extends']['parts']), 'CLASS')

            # Create 'Class EXTENDS AnotherClass' relationship
            if not self.graph.find_relationship(node['name']['name'], 'CLASS', '\\'.join(node['extends']['parts']), 'CLASS', 'EXTENDS'):
                self.graph.create_relationship(node['name']['name'], 'CLASS', '\\'.join(node['extends']['parts']), 'CLASS', 'EXTENDS')   

        # If class contains "implements"
        if node['implements']:
            for interface in node['implements']:
                # Create implemented 'CLASS' node
                if not self.graph.find_node('\\'.join(interface['parts']), 'CLASS'):
                    self.graph.create_node('\\'.join(interface['parts']), 'CLASS')

                # Create 'Class IMPLEMENTS AnotherClass' relationship
                if not self.graph.find_relationship(node['name']['name'], 'CLASS', '\\'.join(interface['parts']), 'CLASS', 'IMPLEMENTS'):
                    self.graph.create_relationship(node['name']['name'], 'CLASS', '\\'.join(interface['parts']), 'CLASS', 'IMPLEMENTS')     

        # Deal with "stmt"s inside the class
        if node['stmts']:
            # "statement" represents each line inside the class
            for statement in node['stmts']:
                if statement['nodeType'] == 'Stmt_ClassMethod':
                    self.stmt_class_method(statement, node['name']['name'], 'CLASS', 'IS_CLASS_METHOD')

    # Describes a class method
    def stmt_class_method(self, node, parent_node=None, parent_node_type=None, relationship_type=None):
        # Create 'CLASS_METHOD' node
        if not self.graph.find_node(node['name']['name'], 'CLASS_METHOD'):
            self.graph.create_node(node['name']['name'], 'CLASS_METHOD')

        # Create 'CLASS_METHOD IS_CLASS_METHOD of Class' relatioship
        if not self.graph.find_relationship(parent_node, parent_node_type, node['name']['name'], 'CLASS_METHOD', relationship_type):
            self.graph.create_relationship(parent_node, parent_node_type, node['name']['name'], 'CLASS_METHOD', relationship_type)   
