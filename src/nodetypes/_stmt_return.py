'''
    Describes a return statement.

    e.g. return testFunc($user, $password);
    e.g. return false;

    HOW IT WORKS!
    1.) Based on the nodeType it calls the relavant nodeType method to establish the node. 
'''
def stmt_return(self, expr, parent_node, parent_node_type, scope):
    # If the retrun statement is a Function call
    if expr['nodeType'] == 'Expr_FuncCall':
        self.expr_func_call(expr, parent_node, parent_node_type, scope, 'FUNCTION_CALL')
    # If the retrun statement is a Method call
    elif expr['nodeType'] == 'Expr_MethodCall':
        self.expr_method_call(expr, parent_node, parent_node_type, scope)