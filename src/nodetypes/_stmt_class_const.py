# Describes a class constant 
# e.g. "const PREVIEWCOLUMNSLIMIT = 10;"
def stmt_class_const(self, consts, parent_node, parent_node_type, scope):
    if consts:
        for const in consts:
            # Create 'CLASS_CONSTANT' node
            if not self.graph.find_node(const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope)):
                self.graph.create_node(const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope))

            # Create 'Class -> IS_CLASS_CONSTANT -> CLASS_CONSTANT'
            if not self.graph.find_relationship(parent_node, parent_node_type, const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope), 'IS_CLASS_CONSTANT'):
                self.graph.create_relationship(parent_node, parent_node_type, const['name']['name'], '{scope}:CLASS_CONSTANT'.format(scope=scope), 'IS_CLASS_CONSTANT')
