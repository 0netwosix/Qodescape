from utils.support import Print

# Describes a Else If block
def stmt_else_if(self, slice, parent_node, parent_node_type, scope):
    if slice['attributes']['startLine']:
        else_if_node_type = 'ELSEIF:{scope}'.format(scope=scope)
        else_if_node_name = self.generate_block_name_by_line(slice['attributes']['startLine'], 'ELSEIF')

        # Create ElseIf block node
        if not self.graph.find_node(else_if_node_name, else_if_node_type):
            self.graph.create_node(else_if_node_name, else_if_node_type)

        # Create ElseIf_block relationship with parent
        if not self.graph.find_relationship(parent_node, parent_node_type, else_if_node_name, else_if_node_type, 'ELSEIF_BLOCK'):
            self.graph.create_relationship(parent_node, parent_node_type, else_if_node_name, else_if_node_type, 'ELSEIF_BLOCK')

        # Describes statements inside the ELSEIF block
        if slice['stmts']:
            for stmt in slice['stmts']:
                # If it is a If block
                if stmt['nodeType'] == 'Stmt_If':
                    self.stmt_if(stmt, else_if_node_name, else_if_node_type, '{parent_scope}'.format(parent_scope=scope))
                elif stmt['nodeType'] == 'Stmt_Expression':
                    self.stmt_expression(stmt['expr'], else_if_node_name, else_if_node_type, '{parent_scope}'.format(parent_scope=scope))
    else:
        Print.error_print('[404]', 'Issue in "ElseIf[attributes]"')