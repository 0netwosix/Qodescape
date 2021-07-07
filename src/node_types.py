#!/usr/bin/python3

from utils.support import Print

class NodeType:
    def __init__(self, graph):
        self.graph = graph

    def stmt_expression(self, expr, parent_node, parent_node_type):
        if expr['nodeType'] == 'Expr_Assign':
            # Create the variable and its relationship with the parent node
            if expr['var']['nodeType'] == 'Expr_Variable':
                self.expr_variable(expr, parent_node, parent_node_type, parent_node)

            ''' Following describes the value of above variable
            '''
            # If the value of above variable is a "String"
            if expr['expr']['nodeType'] == 'Scalar_String':
                # Need to decide
                pass
            # If the value of the above variable is a "Function call"
            elif expr['expr']['nodeType'] == 'Expr_FuncCall':
                self.expr_func_call(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), parent_node)
            # If the value of the above variable is similar to "$GET['id']"
            elif expr['expr']['nodeType'] == 'Expr_ArrayDimFetch':
                self.expr_array_dim_fetch(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), 'ASSIGNS', parent_node, expr['expr']['var']['name'])
            # If the value of the above variable is similar to "select * from `products` where productCode='$prodCode'"
            elif expr['expr']['nodeType'] == 'Scalar_Encapsed':
                self.scalar_encapsed(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), 'ASSIGNS', parent_node)

        elif expr['nodeType'] == 'Expr_FuncCall':
            self.expr_func_call(expr, parent_node, parent_node_type, parent_node)
        elif expr['nodeType'] == 'Expr_AssignOp_Concat':
            if expr['var']['nodeType'] == 'Expr_Variable':
                # Create the variable and its relationship with the parent node
                self.expr_variable(expr, parent_node, parent_node_type, parent_node)

                ''' Following describes the value of above variable
                '''
                # If the value of the above variable is similar to "<pre>Hello ${name}</pre>";
                if expr['expr']['nodeType'] == 'Scalar_Encapsed':
                    self.scalar_encapsed(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), 'ASSIGNS', parent_node)

    # Describes "echo()"
    def stmt_echo(self, exprs, parent_node, parent_node_type, scope):
        if exprs:
            for expr in exprs:
                if expr['nodeType'] == 'Expr_Variable':
                    # Check if the parent node is available
                    if self.graph.find_node(parent_node, parent_node_type):
                        # Check if the variable is available
                        if self.graph.find_node(expr['name'], '{scope}:VARIABLE'.format(scope=scope)):
                            # Check if 'ECHO' relationship exists
                            if not self.graph.find_relationship(parent_node, parent_node_type, expr['name'], '{scope}:VARIABLE'.format(scope=scope), 'ECHO'):
                                self.graph.create_relationship(parent_node, parent_node_type, expr['name'], '{scope}:VARIABLE'.format(scope=scope), 'ECHO')
                        else:
                            Print.error_print('[ERROR]', 'Node not found: {}'.format(expr['name']))
                    else:
                        Print.error_print('[ERROR]', 'Node not found: {}'.format(parent_node))

    # Describes a value like "<pre>Hello ${name}</pre>";
    def scalar_encapsed(self, expr, parent_node, parent_node_type, relationship_type, scope):
        if expr['parts']:
            # Loop through the parts of the string
            for part in expr['parts']:
                if part['nodeType'] == 'Expr_Variable':
                    # This variable must have a node at this point, therefore it is not going to create one
                    # as a result we can't call the existing function expr_variable() to handle this.
                    if self.graph.find_node(part['name'], '{scope}:VARIABLE'.format(scope=scope)):
                        # If it has the node, create the relationship with the variable to which it refers.
                        if not self.graph.find_relationship(parent_node, parent_node_type, part['name'], '{scope}:VARIABLE'.format(scope=scope), relationship_type):
                            self.graph.create_relationship(parent_node, parent_node_type, part['name'], '{scope}:VARIABLE'.format(scope=scope), relationship_type)
                    else:
                        Print.error_print('[ERROR]', 'Node not found: {}'.format(part['name']))

    # Describes $_GET[], $_POST[], $_REQUEST[] statements
    def expr_array_dim_fetch(self, expr, parent_node, parent_node_type, relationship_type, scope, array_type):
        if array_type == '_GET' or array_type == '_REQUEST': 
            if expr['dim']['nodeType'] == 'Scalar_String':
                # Create the node
                if not self.graph.find_node('{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type)):
                    self.graph.create_node('{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type))

                # Create the relationship
                if not self.graph.find_relationship(parent_node, parent_node_type, '{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type), relationship_type):
                    self.graph.create_relationship(parent_node, parent_node_type, '{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type), relationship_type)
                
    # Create a function call relationship in > "$result = mysqli_query($con, $query);"
    # It creates just the function call, not the function defineition node
    def expr_func_call(self, expr, parent_node, parent_node_type, scope):
        # Create "FUNCTION_CALL" node
        if not self.graph.find_node(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope)):
            self.graph.create_node(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope))

        # Create "FUNCTION_CALL" relationship
        if not self.graph.find_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), 'FUNCTION_CALL'):
            self.graph.create_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), 'FUNCTION_CALL')

        if expr['args']:
            for argument in expr['args']:
                # If the argument is a variable
                if 'nodeType' in argument['value'] and argument['value']['nodeType'] == 'Expr_Variable':
                    if 'name' in argument['value']:
                        # Create argument node if it is not there
                        if not self.graph.find_node(argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope)):
                            self.graph.create_node(argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope))

                        # Create the "IS_ARGUMENT" relationship
                        if not self.graph.find_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT'):
                            self.graph.create_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT')
                # If the argument is a $_GET kind of statement
                elif 'nodeType' in argument['value'] and argument['value']['nodeType'] == 'Expr_ArrayDimFetch':
                    self.expr_array_dim_fetch(argument['value'], " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), 'IS_ARGUMENT', scope, argument['value']['var']['name'])
                # If the argument is a string concat like "shell_exec( 'ping  ' . $target )"
                elif 'nodeType' in argument['value'] and argument['value']['nodeType'] == 'Expr_BinaryOp_Concat':
                    # Read left values of the concatanation
                    if 'nodeType' in argument['value']['left']:
                        if argument['value']['left']['nodeType'] == 'Expr_Variable':
                            # Check if the node exists
                            if self.graph.find_node(argument['value']['left']['name'], '{scope}:VARIABLE'.format(scope=scope)):
                                # Check if the relationship exists
                                if not self.graph.find_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['left']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT'):
                                    self.graph.create_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['left']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT')
                    
                    # Read right values of the concatanation
                    if 'nodeType' in argument['value']['right']: 
                        if argument['value']['right']['nodeType'] == 'Expr_Variable':
                            # Check if the node exists
                            if self.graph.find_node(argument['value']['right']['name'], '{scope}:VARIABLE'.format(scope=scope)):
                                # Check if the relationship exists
                                if not self.graph.find_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['right']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT'):
                                    self.graph.create_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['right']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT')


    # Create a variable and its relationship
    def expr_variable(self, expr, parent_node, parent_node_type, scope):
        # Create the variable implementing a relationship with the parent
        if not self.graph.find_node(expr['var']['name'], '{scope}:VARIABLE'.format(scope=scope)):
            self.graph.create_node(expr['var']['name'], '{scope}:VARIABLE'.format(scope=scope))

        # Create the relationship with the parent
        if not self.graph.find_relationship(parent_node, parent_node_type, expr['var']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_VARIABLE'):
            self.graph.create_relationship(parent_node, parent_node_type, expr['var']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_VARIABLE')

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
                        Print.error_print('[ERROR]', 'Different "nodeType": {}'.format(node['nodeType']))
            else:
                Print.error_print('[ERROR]', 'Last list element is not a "Class" node: {}'.format(stmts[-1]['nodeType']))

    # Describes "class ClassName extends AnotherClass implements SomeOtherClass"
    def stmt_class(self, node, parent_node, parent_node_type, relationship_type):
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
                    self.stmt_class_method(statement, node['name']['name'], 'CLASS', 'IS_CLASS_METHOD', node['name']['name'])

    # Describes a class method
    def stmt_class_method(self, node, parent_node, parent_node_type, relationship_type, scope):
        # Create 'CLASS_METHOD' node
        if not self.graph.find_node(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope)):
            self.graph.create_node(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope))

        # Create 'CLASS_METHOD IS_CLASS_METHOD of Class' relatioship
        if not self.graph.find_relationship(parent_node, parent_node_type, node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), relationship_type):
            self.graph.create_relationship(parent_node, parent_node_type, node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), relationship_type)   
