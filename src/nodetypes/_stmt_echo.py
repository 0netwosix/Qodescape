from utils.support import Print

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