from utils import Print

'''
    Describes echo function.

    e.g.1. echo($user)
    e.g.2. echo(getUser())

    HOW IT WORKS!
    1.) If it is echoing a variable,
        1.1) It checks whether the parent node exists with received labels. If yes it proceeds and else it will
        raise an error.
        1.2) In order to echo a variable it should be defined at this point. So it will check the existance of the variable node 
        with following labels.If yes it proceeds and else it will raise and error.
            - {scope:VARIABLE}
        1.3.) Then it creates a "ECHO" relationship between the parent and the echoing variable as follows.
            - relationship_types = ECHO
            - (parent_node)-[ECHO]->(user:{scope:VARIABLE})
    2.) If it is echoing a function call,
        2.1) It checks whether the parent node exists with received labels. If yes it proceeds and else it will
        raise an error.
        2.2) It creates the "getUser" node with following labels it is not there already.
            - "expr_function_call()" handles flow and create the node and relationship as follows.
            - (parent_node)-[FUNCTION_CALL]->(getUser:{scope:FUNCTION_CALL})
        2.3.) Then it creates a "ECHO" relationship between the parent and the echoing function call as follows.
            - relationship_types = ECHO
            - (parent_node)-[ECHO]->(getUser:{scope:FUNCTION_CALL}) 
'''
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
                            self.graph.create_echo_relationship(parent_node, parent_node_type, expr['name'], '{scope}:VARIABLE'.format(scope=scope), 'ECHO')
                    else:
                        Print.error_print('[404]', 'Node not found: {}'.format(expr['name']))
                else:
                    Print.error_print('[404]', 'Node not found: {}'.format(parent_node))
            # If Echo ing a function call
            elif expr['nodeType'] == 'Expr_FuncCall':
                # Check if the parent node is available
                if self.graph.find_node(parent_node, parent_node_type):
                    # Create the function_call node if not available in the scope
                    self.expr_func_call(expr, parent_node, parent_node_type, scope, 'IS_FUNCTION_CALL')

                    # Check if 'ECHO' relationship exists
                    if not self.graph.find_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), 'ECHO'):
                        self.graph.create_echo_relationship(parent_node, parent_node_type, " ".join(expr['name']['parts']), '{scope}:FUNCTION_CALL'.format(scope=scope), 'ECHO')
                else:
                    Print.error_print('[404]', 'Node not found: {}'.format(parent_node))