from utils.support import Print

# Describes a While block
def stmt_while(self, slice, parent_node, parent_node_type, scope):
    if slice['cond']['attributes']['startLine']:
        while_node_type = 'WHILE:{scope}'.format(parent_node=parent_node, scope=scope)
        while_node_name = self.generate_block_name_by_line(slice['cond']['attributes']['startLine'], 'WHILE')

        # Create While block node
        if not self.graph.find_node(while_node_name, while_node_type):
            self.graph.create_node(while_node_name, while_node_type)

        # Create While_block relationship with parent
        if not self.graph.find_relationship(parent_node, parent_node_type, while_node_name, while_node_type, 'WHILE_BLOCK'):
            self.graph.create_relationship(parent_node, parent_node_type, while_node_name, while_node_type, 'WHILE_BLOCK')

        # Describes statements inside the WHILE block
        if slice['stmts']:
            for stmt in slice['stmts']:
                pass
    else:
        Print.error_print('[ERROR]', 'Issue in "While[conditions][attributes]"')