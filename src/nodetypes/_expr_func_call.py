from utils.support import Print

'''
    Describes a function call relationship like in e.g.
    It creates just the function call, not the function defineition node.
    Function call is a call for a function that is defined in another file.

    e.g. $result = mysqli_query($con, $query);

    TODO: 
        1. Call a generalized function to map nodes in args.

    HOW IT WORKS!
    1.) It creates "mysqli_query" node with following labels if it is not there already.
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - FUNCTION_CALL
    - Node
        - mysqli_query:{scope:FUNCTION_CALL}
    2.) Then it creates the following relationship if it does not exist.
        - relationship_types = IS_ARGUMENT, FUNCTION_CALL, ASSIGNS
        - (parent_node)-[relationship_type]->(mysqli_query:{scope:FUNCTION_CALL})
    3.) Once node and it's relationship is created, it looks at it's arguments.
        3.1.) Based on the nodeType of each of the argument, it calls the relavant nodeType method to 
        establish the node and the relationship. 
            - If the argument nodeType is "Expr_Variable",
                - It should be defined as a method variable or a method parameter.
                - Therefore, first it looks at "VARIABLE"s in the same scope, if not found,
                - It looks at "PARAM"s in the same scope,
                - And creates the following relationship. 
                    - (mysqli_query:{scope:FUNCTION_CALL})-[IS_ARGUMENT]->(argument node)
                - If it is not found in "VARIABLE"s or "PARAM"s, it will raise and error and continue.
            - If the argument nodeType is "Expr_FuncCall",
                - It calls "expr_func_call()"
            - If the argument nodeType is "Expr_ArrayDimFetch",
                - It calls "expr_array_dim_fetch()"
'''
def expr_func_call(self, expr, parent_node, parent_node_type, scope, relationship_type):
    # Create "FUNCTION_CALL" node
    if not self.graph.find_node(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope)):
        self.graph.create_node(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope))

    # Create "FUNCTION_CALL" relationship
    if not self.graph.find_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), relationship_type):
        self.graph.create_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), relationship_type)

    if expr['args']:
        for argument in expr['args']:
            # If the argument is a variable
            if 'nodeType' in argument['value'] and argument['value']['nodeType'] == 'Expr_Variable':
                if 'name' in argument['value']:
                    # If argument is a variable, there should be a varibale defined earlier
                    if self.graph.find_node(argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope)):
                        # Create the "IS_ARGUMENT" relationship
                        if not self.graph.find_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT'):
                            self.graph.create_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT')
                    # If it is not defined it should be function's arguments
                    elif self.graph.find_node(argument['value']['name'], '{scope}:PARAM'.format(scope=scope)):
                        # Create the "IS_ARGUMENT" relationship
                        if not self.graph.find_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['name'], '{scope}:PARAM'.format(scope=scope), 'IS_ARGUMENT'):
                            self.graph.create_relationship(" ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), argument['value']['name'], '{scope}:PARAM'.format(scope=scope), 'IS_ARGUMENT')
                    # If there is neither a Variable nor Param, it should be an error
                    else:
                        Print.error_print('[404]', 'Node not found: {}'.format(argument['value']['name']))
            # If the argument is again a Function call
            elif 'nodeType' in argument['value'] and argument['value']['nodeType'] == 'Expr_FuncCall':
                self.expr_func_call(argument['value'], " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), scope, 'IS_ARGUMENT')
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
