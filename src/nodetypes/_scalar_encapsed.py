from utils.support import Print

# Describes a value like "<pre>Hello ${name}</pre>";
def scalar_encapsed(self, expr, parent_node, parent_node_type, relationship_type, scope):
    if expr['parts']:
        # Loop through the parts of the string
        for part in expr['parts']:
            if part['nodeType'] == 'Expr_Variable':
                # This variable must have a node at this point, therefore it is not going to create one
                # as a result we can't call the existing function expr_variable() to handle this.
                if self.graph.find_node(part['name'], '{scope}:VARIABLE'.format(scope=scope)):
                    # If it has the node, create the relationship with the variable to which it refers.
                    if not self.graph.find_relationship(parent_node, parent_node_type, part['name'], '{scope}:VARIABLE'.format(scope=scope), relationship_type):
                        self.graph.create_relationship(parent_node, parent_node_type, part['name'], '{scope}:VARIABLE'.format(scope=scope), relationship_type)
                else:
                    Print.error_print('[ERROR]', 'Node not found: {}'.format(part['name']))