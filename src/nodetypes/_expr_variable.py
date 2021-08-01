# Create a variable and its relationship
def expr_variable(self, expr, parent_node, parent_node_type, scope):
    # Create the variable implementing a relationship with the parent
    if not self.graph.find_node(expr['var']['name'], '{scope}:VARIABLE'.format(scope=scope)):
        self.graph.create_node(expr['var']['name'], '{scope}:VARIABLE'.format(scope=scope))

    # Create the relationship with the parent
    if not self.graph.find_relationship(parent_node, parent_node_type, expr['var']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_VARIABLE'):
        self.graph.create_relationship(parent_node, parent_node_type, expr['var']['name'], '{scope}:VARIABLE'.format(scope=scope), 'IS_VARIABLE')
