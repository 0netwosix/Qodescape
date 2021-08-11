from utils import Print

'''
    Describes a value like in the e.g.

    e.g. "<pre>Hello ${name}</pre>";

    HOW IT WORKS!
    1.) It cheks for a "name" node with following labels.
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - VARIABLE
    2.) At this point of the code, above node should be present.
        2.1.) If so it creates the following relationship if it does not exist.
            - relationship_types = ASSIGNS
            - (parent_node)-[ASSIGNS]->(name:{scope:VARIABLE}) 
        2.2.) If not it will raise and error.
'''
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
                    Print.error_print('[404]', 'Node not found: {}'.format(part['name']))