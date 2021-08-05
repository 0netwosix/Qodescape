from utils.support import Print

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
                if stmt['nodeType'] == 'Stmt_Expression':
                    self.stmt_expression(stmt['expr'], if_node_name, if_node_type, '{parent_scope}'.format(parent_scope=scope))
                # If it imports global variables 
                elif stmt['nodeType'] == 'Stmt_Global':
                    self.stmt_global(stmt['vars'], if_node_name, if_node_type, '{parent_scope}'.format(parent_scope=scope))
                # If the statement is a Return statement
                elif stmt['nodeType'] == 'Stmt_Return':
                    # self.stmt_return(stmt['expr'], if_node_name, if_node_type, '{this_node}:{parent_scope}'.format(this_node=if_node_name, parent_scope=scope))
                    self.stmt_return(stmt['expr'], if_node_name, if_node_type, '{parent_scope}'.format(parent_scope=scope))
                # If the statement is a While block
                elif stmt['nodeType'] == 'Stmt_While':
                    self.stmt_while(stmt, if_node_name, if_node_type, '{parent_scope}'.format(parent_scope=scope))

        # Describes the Else block
        if slice['else']:
            if slice['else']['nodeType'] == 'Stmt_Else':
                # self.stmt_else(slice['else'], if_node_name, if_node_type, '{this_node}:{parent_scope}'.format(this_node=if_node_name, parent_scope=scope))
                self.stmt_else(slice['else'], if_node_name, if_node_type, '{parent_scope}'.format(parent_scope=scope))
    
        # Describes the ELSE IF block
        if slice['elseifs']:
            pass
    
    else:
        Print.error_print('[404]', 'Issue in "If[conditions][attributes]"')