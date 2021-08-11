from utils.support import Print

'''
    Create a method call relationship like in e.g. s.
    It creates just the method call, not the method defineition node.
    Method call is a call for a method that is defined in the same file.

    e.g.1. $this->user_signup_with_confirmation($user, $notify);
    e.g.2. $DB->set_field("something"); This type of statement is also comes under this category.

    TODO: 
        1.) Create a relationship with original "Method" when it is a "Expr_MethodCall".
        - See Notion.
        2.) Call a generalized function to map nodes in args.

    HOW IT WORKS!
    - It works identical to "expr_func_call()".
    - Only the labels would change.
    - Scope
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - METHOD_CALL
    - Node
        - user_signup_with_confirmation:{scope:METHOD_CALL}
    - Relationship
        - (parent_node)-[METHOD_CALL]->(user_signup_with_confirmation:{scope:METHOD_CALL})
    - Args Relationship
        - (user_signup_with_confirmation:{scope:METHOD_CALL})-[IS_ARGUMENT]->(argument node)
'''
def expr_method_call(self, expr, parent_node, parent_node_type, scope):
    # Create "METHOD_CALL" node
    if not self.graph.find_node(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope)):
        self.graph.create_node(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope))

    # Create "METHOD_CALL" relationship
    if not self.graph.find_relationship(parent_node, parent_node_type, expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), 'METHOD_CALL'):
        self.graph.create_relationship(parent_node, parent_node_type, expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), 'METHOD_CALL')

    if expr['args']:
        for argument in expr['args']:
            # If the argument is a variable
            if 'nodeType' in argument['value'] and argument['value']['nodeType'] == 'Expr_Variable':
                if 'name' in argument['value']:
                    # If argument is a variable, there should be a varibale defined earlier
                    if self.graph.find_node(argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope)):
                        # Create the "IS_ARGUMENT" relationship
                        if not self.graph.find_relationship(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT'):
                            self.graph.create_relationship(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), argument['value']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT')
                    # If it is not defined it should be function's parameter
                    elif self.graph.find_node(argument['value']['name'], '{scope}:PARAM'.format(scope=scope)):
                        # Create the "IS_ARGUMENT" relationship
                        if not self.graph.find_relationship(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), argument['value']['name'], '{scope}:PARAM'.format(scope=scope), 'IS_ARGUMENT'):
                            self.graph.create_relationship(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), argument['value']['name'], '{scope}:PARAM'.format(scope=scope), 'IS_ARGUMENT')
                    # If there is neither a Variable nor Param, it should be an error
                    else:
                        Print.error_print('[404]', 'Node not found: {}'.format(argument['value']['name']))

            # If the argument is a $_GET kind of statement
            elif 'nodeType' in argument['value'] and argument['value']['nodeType'] == 'Expr_ArrayDimFetch':
                self.expr_array_dim_fetch(argument['value'], expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), 'IS_ARGUMENT', scope, argument['value']['var']['name'])
            # If the argument is a string concat like "shell_exec( 'ping  ' . $target )"
            elif 'nodeType' in argument['value'] and argument['value']['nodeType'] == 'Expr_BinaryOp_Concat':
                # Read left values of the concatanation
                if 'nodeType' in argument['value']['left']:
                    if argument['value']['left']['nodeType'] == 'Expr_Variable':
                        # Check if the node exists
                        if self.graph.find_node(argument['value']['left']['name'], '{scope}:VARIABLE'.format(scope=scope)):
                            # Check if the relationship exists
                            if not self.graph.find_relationship(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), argument['value']['left']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT'):
                                self.graph.create_relationship(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), argument['value']['left']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT')
                
                # Read right values of the concatanation
                if 'nodeType' in argument['value']['right']: 
                    if argument['value']['right']['nodeType'] == 'Expr_Variable':
                        # Check if the node exists
                        if self.graph.find_node(argument['value']['right']['name'], '{scope}:VARIABLE'.format(scope=scope)):
                            # Check if the relationship exists
                            if not self.graph.find_relationship(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), argument['value']['right']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT'):
                                self.graph.create_relationship(expr['name']['name'], '{scope}:METHOD_CALL'.format(scope=scope), argument['value']['right']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_ARGUMENT')
