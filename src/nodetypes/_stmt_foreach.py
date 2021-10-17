from utils import Print

'''
    Describes a Foreach block.

    TODO: 
        1. Call a generalized function to map nodes in stmts.

    HOW IT WORKS!
    
'''
def stmt_foreach(self, slice, parent_node, parent_node_type, scope):
    if slice['attributes']['startLine']:
        foreach_node_type = 'FOREACH:{scope}'.format(scope=scope)
        foreach_node_name = self.generate_block_name_by_line(slice['attributes']['startLine'], 'FOREACH')

        # Create Foreach block node
        if not self.graph.find_node(foreach_node_name, foreach_node_type):
            self.graph.create_node(foreach_node_name, foreach_node_type)

        # Create Foreach_block relationship with parent
        if not self.graph.find_relationship(parent_node, parent_node_type, foreach_node_name, foreach_node_type, 'FOREACH_BLOCK'):
            self.graph.create_relationship(parent_node, parent_node_type, foreach_node_name, foreach_node_type, 'FOREACH_BLOCK')

        # Describes statements inside the FOREACH block
        if slice['stmts']:
            for stmt in slice['stmts']:
                if stmt['nodeType'] == 'Stmt_Expression':
                    self.stmt_expression(stmt['expr'], foreach_node_name, foreach_node_type, '{parent_scope}'.format(parent_scope=scope))
                elif stmt['nodeType'] == 'Stmt_If':
                    self.stmt_if(stmt, foreach_node_name, foreach_node_type, '{parent_scope}'.format(parent_scope=scope))
            
    else:
        Print.error_print('[404]', 'Issue in "Foreach[attributes]"')