from utils import Print

'''
    Describes a While block.

    TODO: 
        1. Call a generalized function to map nodes in stmts.

    HOW IT WORKS!
    1.) It creates a custom node name for the "while" node as it can have multiple "while" nodes in a single scope.
        - WHILE.name = WHILE_line_127
    2.) Then it creates "WHILE_line_127" node with following labels.
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - WHILE
    3.) Then it creates the following relationship if it does not exist.
        - relationship_types = WHILE_BLOCK
        - (parent_node)-[WHILE_BLOCK]->(WHILE_line_127:{scope:WHILE})
    4.) Once done, it looks at the statements inside the "while" block and calls the relavant nodeType method accordingly.
        - If it is a "Stmt_Expression", it calls "stmt_expression()".
        - ...
'''
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
        Print.error_print('[404]', 'Issue in "While[conditions][attributes]"')