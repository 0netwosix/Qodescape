'''
    Create a variable and its relationship.

    e.g. $product = 'test';

    HOW IT WORKS!
    1.) It creates a "product" node with following labels if it is not there already.
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - VARIABLE
    2.) Then it creates the following relationship.
        - relationship_types = IS_VARIABLE
        - (parent_node)-[IS_VARIABLE]->(product:{scope:VARIABLE})
'''
def expr_variable(self, expr, parent_node, parent_node_type, scope, variable_type, relationship_type):
    # Create the variable implementing a relationship with the parent
    if not self.graph.find_node(expr['var']['name'], '{scope}:{variable_type}'.format(scope=scope, variable_type=variable_type)):
        self.graph.create_node(expr['var']['name'], '{scope}:{variable_type}'.format(scope=scope, variable_type=variable_type))

    # Create the relationship with the parent
    if not self.graph.find_relationship(parent_node, parent_node_type, expr['var']['name'], '{scope}:{variable_type}'.format(scope=scope, variable_type=variable_type), relationship_type):
        self.graph.create_relationship(parent_node, parent_node_type, expr['var']['name'], '{scope}:{variable_type}'.format(scope=scope, variable_type=variable_type), relationship_type)
