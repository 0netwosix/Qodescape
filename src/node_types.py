#!/usr/bin/python3

from utils.support import Print

class NodeType:
    def __init__(self, graph):
        self.graph = graph

    # Generate a label looks like "if_line_26", "while_line_26"
    # To seperately identify each block (when having multiple "if" in same file)
    def generate_block_name_by_line(self, line_number, block_type):
        return ('{block_type}_line_{line_number}'.format(block_type=block_type, line_number=line_number))

    # Describes a If block
    def stmt_if(self, slice, parent_node, parent_node_type, scope):
        if slice['cond']['attributes']['startLine']:
            if_node_type = '{scope}:IF'.format(scope=scope)
            if_node_name = self.generate_block_name_by_line(slice['cond']['attributes']['startLine'], 'IF')

            # Create If block node
            if not self.graph.find_node(if_node_name, if_node_type):
                self.graph.create_node(if_node_name, if_node_type)

            # Create If_block relationship with parent
            if not self.graph.find_relationship(parent_node, parent_node_type, if_node_name, if_node_type, 'IF_BLOCK'):
                self.graph.create_relationship(parent_node, parent_node_type, if_node_name, if_node_type, 'IF_BLOCK')

            # Describes statements inside the IF block
            if slice['stmts']:
                for stmt in slice['stmts']:
                    # If the statement is a While block
                    if stmt['nodeType'] == 'Stmt_While':
                        self.stmt_while(stmt, if_node_name, if_node_type, '{this_node}:{parent_scope}'.format(this_node=if_node_name, parent_scope=parent_node))

            # Describes the Else block
            if slice['else']:
                if slice['else']['nodeType'] == 'Stmt_Else':
                    self.stmt_else(slice['else'], if_node_name, if_node_type, '{this_node}:{parent_scope}'.format(this_node=if_node_name, parent_scope=parent_node))
        
            # Describes the ELSE IF block
            if slice['elseifs']:
                pass
        
        else:
            Print.error_print('[ERROR]', 'Issue in "If[conditions][attributes]"')

    # Describes a Else block
    def stmt_else(self, slice, parent_node, parent_node_type, scope):
        if slice['attributes']['startLine']:
            else_node_type = 'ELSE:{scope}'.format(parent_node=parent_node, scope=scope)
            else_node_name = self.generate_block_name_by_line(slice['attributes']['startLine'], 'ELSE')

             # Create Else block node
            if not self.graph.find_node(else_node_name, else_node_type):
                self.graph.create_node(else_node_name, else_node_type)

            # Create Else_block relationship with parent
            if not self.graph.find_relationship(parent_node, parent_node_type, else_node_name, else_node_type, 'ELSE_BLOCK'):
                self.graph.create_relationship(parent_node, parent_node_type, else_node_name, else_node_type, 'ELSE_BLOCK')

            # Describes statements inside the ELSE block
            if slice['stmts']:
                for stmt in slice['stmts']:
                    # If the statement is an echo
                    if stmt['nodeType'] == 'Stmt_Echo':
                        self.stmt_echo(stmt['exprs'], else_node_name, else_node_type, '{this_node}:{parent_scope}'.format(this_node=else_node_name, parent_scope=scope))
        else:
            Print.error_print('[ERROR]', 'Issue in "Else[attributes]"')


    # Describes a While block
    def stmt_while(self, slice, parent_node, parent_node_type, scope):
        if slice['cond']['attributes']['startLine']:
            while_node_type = 'WHILE:{scope}'.format(parent_node=parent_node, scope=scope)
            while_node_name = self.generate_block_name_by_line(slice['cond']['attributes']['startLine'], 'WHILE')

            # Create While block node
            if not self.graph.find_node(while_node_name, while_node_type):
                self.graph.create_node(while_node_name, while_node_type)

            # Create While_block relationship with parent
            if not self.graph.find_relationship(parent_node, parent_node_type, while_node_name, while_node_type, 'WHILE_BLOCK'):
                self.graph.create_relationship(parent_node, parent_node_type, while_node_name, while_node_type, 'WHILE_BLOCK')

            # Describes statements inside the WHILE block
            if slice['stmts']:
                for stmt in slice['stmts']:
                    pass
        else:
            Print.error_print('[ERROR]', 'Issue in "While[conditions][attributes]"')
        

    # Describes a whole line inside the code
    # eg: value assignment, function call
    def stmt_expression(self, expr, parent_node, parent_node_type, scope):
        if expr['nodeType'] == 'Expr_Assign':
            variable_decalred = False
            # Create the variable and its relationship with the parent node
            if expr['var']['nodeType'] == 'Expr_Variable':
                self.expr_variable(expr, parent_node, parent_node_type, scope)
                variable_decalred = True
            # Describes "$this->variable = $variable;"
            elif expr['var']['nodeType'] == 'Expr_PropertyFetch':
                if expr['var']['var']['nodeType'] == 'Expr_Variable' and expr['var']['var']['name'] == 'this':
                    tmp_expr = {
                        'var': {
                            'name': expr['var']['name']['name']
                        }
                    }
                    self.expr_variable(tmp_expr, parent_node, parent_node_type, scope)
                    variable_decalred = True

            ''' Following describes the value of above variable
            '''
            # If the varibale node is not created, the value node won't be created as well
            if variable_decalred:
                # If the value of above variable is a "String"
                if expr['expr']['nodeType'] == 'Scalar_String':
                    # Need to decide
                    pass
                # If the value of the above variable is a "Function call"
                elif expr['expr']['nodeType'] == 'Expr_FuncCall':
                    self.expr_func_call(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), scope)
                # If the value of the above variable is similar to "$GET['id']"
                elif expr['expr']['nodeType'] == 'Expr_ArrayDimFetch':
                    self.expr_array_dim_fetch(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), 'ASSIGNS', scope, expr['expr']['var']['name'])
                # If the value of the above variable is similar to "select * from `products` where productCode='$prodCode'"
                elif expr['expr']['nodeType'] == 'Scalar_Encapsed':
                    self.scalar_encapsed(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), 'ASSIGNS', scope)

        elif expr['nodeType'] == 'Expr_FuncCall':
            self.expr_func_call(expr, parent_node, parent_node_type, scope)
        elif expr['nodeType'] == 'Expr_AssignOp_Concat':
            if expr['var']['nodeType'] == 'Expr_Variable':
                # Create the variable and its relationship with the parent node
                self.expr_variable(expr, parent_node, parent_node_type, scope)

                ''' Following describes the value of above variable
                '''
                # If the value of the above variable is similar to "<pre>Hello ${name}</pre>";
                if expr['expr']['nodeType'] == 'Scalar_Encapsed':
                    self.scalar_encapsed(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), 'ASSIGNS', scope)

    # Describes "echo()"
    def stmt_echo(self, exprs, parent_node, parent_node_type, scope):
        if exprs:
            for expr in exprs:
                # If Echo ing a variable
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
                # If Echo ing a function call
                elif expr['nodeType'] == 'Expr_FuncCall':
                    # Check if the parent node is available
                    if self.graph.find_node(parent_node, parent_node_type):
                        # Create the function_call node if not available in the scope
                        self.expr_func_call(expr, parent_node, parent_node_type, scope)

                        # Check if 'ECHO' relationship exists
                        if not self.graph.find_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), 'ECHO'):
                            self.graph.create_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), 'ECHO')
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

    # Describes a global variables in a file. 
    # e.g. "global $CFG;"
    def stmt_global(self, vars, parent_node, parent_node_type, scope):
        # nodeType          -> GLOBAL_VARIABLE
        # relationshipType  -> IS_GLOBAL_VARIABLE
        if vars:
            for var in vars:
                if var['nodeType'] == 'Expr_Variable':
                    # Create 'GLOBAL_VARIABLE' node
                    if not self.graph.find_node(var['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope)):
                        self.graph.create_node(var['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope))

                    # Create 'Filename -> IS_GLOBAL_VARIABLE -> GLOBAL_VARIABLE'
                    if not self.graph.find_relationship(parent_node, parent_node_type, var['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope), 'IS_GLOBAL_VARIABLE'):
                        self.graph.create_relationship(parent_node, parent_node_type, var['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope), 'IS_GLOBAL_VARIABLE')

    # Describes a class constant 
    # e.g. "const PREVIEWCOLUMNSLIMIT = 10;"
    def stmt_class_const(self, consts, parent_node, parent_node_type, scope):
        if consts:
            for const in consts:
                # Create 'CLASS_CONSTANT' node
                if not self.graph.find_node(const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope)):
                    self.graph.create_node(const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope))

                # Create 'Class -> IS_CLASS_CONSTANT -> CLASS_CONSTANT'
                if not self.graph.find_relationship(parent_node, parent_node_type, const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope), 'IS_CLASS_CONSTANT'):
                    self.graph.create_relationship(parent_node, parent_node_type, const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope), 'IS_CLASS_CONSTANT')

    # Describes a protected variable
    # e.g. "protected $feedbackstructure;"
    def stmt_property(self, props, parent_node, parent_node_type, scope):
        if props:
            for prop in props:
                if prop['name']['nodeType'] == 'VarLikeIdentifier':
                    # Create 'PROTECTED_VARIABLE' node
                    if not self.graph.find_node(prop['name']['name'], '{scope}:PROTECTED_VARIABLE'.format(scope=scope)):
                        self.graph.create_node(prop['name']['name'], '{scope}:PROTECTED_VARIABLE'.format(scope=scope))

                    # Create 'Class -> IS_PROTECTED_VARIABLE -> PROTECTED_VARIABLE'
                    if not self.graph.find_relationship(parent_node, parent_node_type, prop['name']['name'], '{scope}:PROTECTED_VARIABLE'.format(scope=scope), 'IS_PROTECTED_VARIABLE'):
                        self.graph.create_relationship(parent_node, parent_node_type, prop['name']['name'], '{scope}:PROTECTED_VARIABLE'.format(scope=scope), 'IS_PROTECTED_VARIABLE')


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

    # Describes "class ClassName extends AnotherClass implements SomeOtherClass"
    def stmt_class(self, node, parent_node, parent_node_type, relationship_type, scope):
        # Labels that denote the scope of the class
        stmt_class_type = '{scope}:CLASS'.format(scope=scope)

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
                elif statement['nodeType'] == 'Stmt_ClassConst':
                    self.stmt_class_const(statement['consts'], node['name']['name'], 'CLASS', node['name']['name'])
                elif statement['nodeType'] == 'Stmt_Property':
                    self.stmt_property(statement['props'], node['name']['name'], 'CLASS', node['name']['name'])

    # Describes a class method
    def stmt_class_method(self, node, parent_node, parent_node_type, relationship_type, scope):
        # Create 'CLASS_METHOD' node
        if not self.graph.find_node(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope)):
            self.graph.create_node(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope))

        # Create 'CLASS_METHOD IS_CLASS_METHOD of Class' relatioship
        if not self.graph.find_relationship(parent_node, parent_node_type, node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), relationship_type):
            self.graph.create_relationship(parent_node, parent_node_type, node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), relationship_type)   

        # Describes method parameters
        if node['params']:
            for param in node['params']:
                if param['var']['nodeType'] == 'Expr_Variable':
                    # Create 'PARAM' node
                    if not self.graph.find_node(param['var']['name'], '{scope}:{class_method}:PARAM'.format(scope=scope, class_method=node['name']['name'])):
                        self.graph.create_node(param['var']['name'], '{scope}:{class_method}:PARAM'.format(scope=scope, class_method=node['name']['name']))

                    # Create 'CLASS_METHOD -> IS_PARAM -> PARAM'
                    if not self.graph.find_relationship(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), param['var']['name'], '{scope}:{class_method}:PARAM'.format(scope=scope, class_method=node['name']['name']), 'IS_PARAM'):
                        self.graph.create_relationship(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), param['var']['name'], '{scope}:{class_method}:PARAM'.format(scope=scope, class_method=node['name']['name']), 'IS_PARAM')

        # Describes the statements inside the method
        if node['stmts']:
            for stmt in node['stmts']:
                if stmt['nodeType'] == 'Stmt_Expression':
                    self.stmt_expression(stmt['expr'], node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), '{scope}:{class_method}'.format(scope=scope, class_method=node['name']['name']))
                elif stmt['nodeType'] == 'Stmt_If':
                    self.stmt_if(stmt, node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), '{scope}:{class_method}'.format(scope=scope, class_method=node['name']['name']))