from utils import Print

'''
    Describes a Else If block.

    TODO: 
        1. Call a generalized function to map nodes in stmts.

    HOW IT WORKS!
    1.) It creates a custom node name for the "else if" node as it can have multiple "else if" nodes in a single scope.
        - ELSEIF.name = ELSEIF_line_127
    2.) Then it creates "ELSEIF_line_127" node with following labels.
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - ELSEIF
    3.) Then it creates the following relationship if it does not exist.
        - relationship_types = ELSEIF_BLOCK
        - (parent_node)-[ELSEIF_BLOCK]->(ELSEIF_line_127:{scope:ELSEIF})
    4.) Once done, it looks at the statements inside the "else if" block and calls the relavant nodeType method accordingly.
        - If it is a "Stmt_Expression", it calls "stmt_expression()".
        - ...
'''
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