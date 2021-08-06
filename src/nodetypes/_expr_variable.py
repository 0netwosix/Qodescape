# Create a variable and its relationship
def expr_variable(self, expr, parent_node, parent_node_type, scope, variable_type, relationship_type):
    # Create the variable implementing a relationship with the parent
    if not self.graph.find_node(expr['var']['name'], '{scope}:{variable_type}'.format(scope=scope, variable_type=variable_type)):
        self.graph.create_node(expr['var']['name'], '{scope}:{variable_type}'.format(scope=scope, variable_type=variable_type))

    # Create the relationship with the parent
    if not self.graph.find_relationship(parent_node, parent_node_type, expr['var']['name'], '{scope}:{variable_type}'.format(scope=scope, variable_type=variable_type), relationship_type):
        self.graph.create_relationship(parent_node, parent_node_type, expr['var']['name'], '{scope}:{variable_type}'.format(scope=scope, variable_type=variable_type), relationship_type)
