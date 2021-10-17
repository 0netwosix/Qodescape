'''
    Describes a whole line inside the code. It can be a assignments operation,
    function call etc.
    This file is also an intermediate place where it calls other node types.

    TODO: 
        1. Try calling the generalized function to map nodes. Would be tricky than in 
        stmts in other nodes.
        2. Need to reasess the whole file.
'''
def stmt_expression(self, expr, parent_node, parent_node_type, scope):
    if expr['nodeType'] == 'Expr_Assign':
        variable_decalred = False
        # Create the variable and its relationship with the parent node
        if expr['var']['nodeType'] == 'Expr_Variable':
            self.expr_variable(expr, parent_node, parent_node_type, scope, 'VARIABLE', 'IS_VARIABLE')
            variable_decalred = True

        # Describes "$this->variable = $variable;"
        # and "$user->password = something();"
        elif expr['var']['nodeType'] == 'Expr_PropertyFetch':
            # Describes "$this->variable = $variable;"
            if expr['var']['var']['nodeType'] == 'Expr_Variable' and expr['var']['var']['name'] == 'this':
                tmp_expr = {
                    'var': {
                        'name': expr['var']['name']['name']
                    }
                }
                self.expr_variable(tmp_expr, parent_node, parent_node_type, scope, 'VARIABLE', 'IS_VARIABLE')
                variable_decalred = True

            # Describes "$user->password = something();"
            elif expr['var']['var']['nodeType'] == 'Expr_Variable' and expr['var']['var']['name'] != 'this':
                '''
                    Describes the following scenario
                    e.g. $user->password = something()

                    Parent node     = $user ('VARIABLE') ('GLOBAL_VARIABLE') ('PARAM')
                    Child node      = password ('PROPERTY')
                    Relationship    = $user -['IS_PROPERTY']-> password
                '''
                # Create the node and relationship
                self.expr_property_fetch_lhs(expr['var'], scope)

                # Handle the assigned value for this nodeType seperately in here
                # Therefore "variable_declared" should be False
                if expr['expr']['nodeType'] == 'Expr_FuncCall':
                    self.expr_func_call(expr['expr'], expr['var']['name']['name'], '{scope}:PROPERTY'.format(scope=scope), scope, 'ASSIGNS')
        
        # Describes "$identity[] = $data->$userextrafield;"
        elif expr['var']['nodeType'] == 'Expr_ArrayDimFetch':
            if not expr['var']['dim']:
                self.expr_variable(expr['var'], parent_node, parent_node_type, scope, 'VARIABLE', 'IS_VARIABLE')

                # Handle the assigned value for this nodeType seperately in here
                # Therefore "variable_declared" should be False
                if expr['expr']['nodeType'] == 'Expr_PropertyFetch':
                    self.expr_property_fetch_rhs(expr['expr'], expr['var']['var']['name'], '{scope}:VARIABLE'.format(scope=scope), scope, 'ASSIGNS')
                elif expr['expr']['nodeType'] == 'Expr_FuncCall':
                    self.expr_func_call(expr['expr'], expr['var']['var']['name'], '{scope}:VARIABLE'.format(scope=scope), scope, 'ASSIGNS')

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
                if expr['var']['nodeType'] == 'Expr_PropertyFetch':
                    self.expr_func_call(expr['expr'], expr['var']['name']['name'], '{scope}:VARIABLE'.format(scope=scope), scope, 'ASSIGNS')
                else:
                    self.expr_func_call(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=scope), scope, 'ASSIGNS')
            # If the value of the above variable is similar to "$GET['id']"
            elif expr['expr']['nodeType'] == 'Expr_ArrayDimFetch':
                self.expr_array_dim_fetch(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), 'ASSIGNS', scope, expr['expr']['var']['name'])
            # If the value of the above variable is similar to "$user->password"
            elif expr['expr']['nodeType'] == 'Expr_PropertyFetch':
                self.expr_property_fetch_rhs(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), scope, 'ASSIGNS')
            # If the value of the above variable is similar to "select * from `products` where productCode='$prodCode'"
            elif expr['expr']['nodeType'] == 'Scalar_Encapsed':
                self.scalar_encapsed(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), 'ASSIGNS', scope)

    elif expr['nodeType'] == 'Expr_FuncCall':
        self.expr_func_call(expr, parent_node, parent_node_type, scope, 'IS_FUNCTION_CALL')
    elif expr['nodeType'] == 'Expr_MethodCall':
        self.expr_method_call(expr, parent_node, parent_node_type, scope)
    elif expr['nodeType'] == 'Expr_AssignOp_Concat':
        if expr['var']['nodeType'] == 'Expr_Variable':
            # Create the variable and its relationship with the parent node
            self.expr_variable(expr, parent_node, parent_node_type, scope, 'VARIABLE', 'IS_VARIABLE')

            ''' Following describes the value of above variable
            '''
            # If the value of the above variable is similar to "<pre>Hello ${name}</pre>";
            if expr['expr']['nodeType'] == 'Scalar_Encapsed':
                self.scalar_encapsed(expr['expr'], expr['var']['name'], '{scope}:VARIABLE'.format(scope=parent_node), 'ASSIGNS', scope)
    elif expr['nodeType'] == 'Expr_StaticCall':
        if expr['class']['nodeType'] == 'Name':
            if "".join(expr['class']['nodeType']) == 'self':
                self.expr_static_call(expr['name'], parent_node, parent_node_type, scope)