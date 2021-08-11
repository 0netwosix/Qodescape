from utils import Print

'''
    Describes a Else block.

    TODO: 
        1. Call a generalized function to map nodes in stmts.

    HOW IT WORKS!
    1.) It creates a custom node name for the "else" node as it can have multiple "else" nodes in a single scope.
        - ELSE.name = ELSE_line_127
    2.) Then it creates "ELSE_line_127" node with following labels.
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - ELSE
    3.) Then it creates the following relationship if it does not exist.
        - relationship_types = ELSE_BLOCK
        - (parent_node)-[ELSE_BLOCK]->(ELSE_line_127:{scope:ELSE})
    4.) Once done, it looks at the statements inside the "else" block and calls the relavant nodeType method accordingly.
        - If it is a "Stmt_Expression", it calls "stmt_expression()".
        - ...
'''
def stmt_else(self, slice, parent_node, parent_node_type, scope):
    if slice['attributes']['startLine']:
        else_node_type = 'ELSE:{scope}'.format(scope=scope)
        else_node_name = self.generate_block_name_by_line(slice['attributes']['startLine'], 'ELSE')

        # Create Else block node
        if not self.graph.find_node(else_node_name, else_node_type):
            self.graph.create_node(else_node_name, else_node_type)

        # Create Else_block relationship with parent
        if not self.graph.find_relationship(parent_node, parent_node_type, else_node_name, else_node_type, 'ELSE_BLOCK'):
            self.graph.create_relationship(parent_node, parent_node_type, else_node_name, else_node_type, 'ELSE_BLOCK')

        # Describes statements inside the ELSE block
        if slice['stmts']:
            for stmt in slice['stmts']:
                # If the statement is an echo
                if stmt['nodeType'] == 'Stmt_Echo':
                    self.stmt_echo(stmt['exprs'], else_node_name, else_node_type, '{parent_scope}'.format(parent_scope=scope))
    else:
        Print.error_print('[404]', 'Issue in "Else[attributes]"')