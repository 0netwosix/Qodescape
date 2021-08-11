'''
    Describes a class constant.

    e.g. const CONSTVALUE = 10;

    HOW IT WORKS!
    1.) It creates "CONSTVALUE" node with following labels if it is not already there.
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - CLASS_CONSTANT
    2.) Then it creates the following relationship if it is not already there.
        - relationship_types = IS_CLASS_CONSTANT
        - (parent_node)-[IS_CLASS_CONSTANT]->(CONSTVALUE:{scope:CLASS_CONST})
'''
def stmt_class_const(self, consts, parent_node, parent_node_type, scope):
    if consts:
        for const in consts:
            # Create 'CLASS_CONSTANT' node
            if not self.graph.find_node(const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope)):
                self.graph.create_node(const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope))

            # Create 'Class -> IS_CLASS_CONSTANT -> CLASS_CONSTANT'
            if not self.graph.find_relationship(parent_node, parent_node_type, const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope), 'IS_CLASS_CONSTANT'):
                self.graph.create_relationship(parent_node, parent_node_type, const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope), 'IS_CLASS_CONSTANT')
