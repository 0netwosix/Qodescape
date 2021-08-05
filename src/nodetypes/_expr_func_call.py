from utils.support import Print

# Create a function call relationship in > "$result = mysqli_query($con, $query);"
# It creates just the function call, not the function defineition node
# Function call is a call for a function that is defined in another file
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
                        Print.error_print('[ERROR]', 'Node not found: {}'.format(argument['value']['name']))

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
