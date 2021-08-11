'''
    Describes a protected variable.

    e.g. protected $testVar;

    HOW IT WORKS!
    1.) It creates "testVar" node with following labels if it does not exist.
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - PROTECTED_VARIABLE
    2.) Then it creates the following relationship if it does not exist.
        - relationship_types = IS_PROTECTED_VARIABLE
        - (parent_node)-[IS_PROTECTED_VARIABLE]->(testVar:{scope:PROTECTED_VARIABLE})
'''
def stmt_property(self, props, parent_node, parent_node_type, scope):
    if props:
        for prop in props:
            if prop['name']['nodeType'] == 'VarLikeIdentifier':
                # Create 'PROTECTED_VARIABLE' node
                if not self.graph.find_node(prop['name']['name'], '{scope}:PROTECTED_VARIABLE'.format(scope=scope)):
                    self.graph.create_node(prop['name']['name'], '{scope}:PROTECTED_VARIABLE'.format(scope=scope))

                # Create 'Class -> IS_PROTECTED_VARIABLE -> PROTECTED_VARIABLE'
                if not self.graph.find_relationship(parent_node, parent_node_type, prop['name']['name'], '{scope}:PROTECTED_VARIABLE'.format(scope=scope), 'IS_PROTECTED_VARIABLE'):
                    self.graph.create_relationship(parent_node, parent_node_type, prop['name']['name'], '{scope}:PROTECTED_VARIABLE'.format(scope=scope), 'IS_PROTECTED_VARIABLE')

