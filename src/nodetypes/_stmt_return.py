# Describes a return statement
# e.g. return validate_internal_user_password($user, $password);
# e.g. return false;
def stmt_return(self, expr, parent_node, parent_node_type, scope):
    # If the retrun statement is a Function call
    if expr['nodeType'] == 'Expr_FuncCall':
        self.expr_func_call(expr, parent_node, parent_node_type, scope, 'FUNCTION_CALL')
    elif expr['nodeType'] == 'Expr_MethodCall':
        self.expr_method_call(expr, parent_node, parent_node_type, scope)