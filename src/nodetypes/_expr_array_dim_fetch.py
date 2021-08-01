# Describes $_GET[], $_POST[], $_REQUEST[] statements
def expr_array_dim_fetch(self, expr, parent_node, parent_node_type, relationship_type, scope, array_type):
    if array_type == '_GET' or array_type == '_REQUEST': 
        if expr['dim']['nodeType'] == 'Scalar_String':
            # Create the node
            if not self.graph.find_node('{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type)):
                self.graph.create_node('{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type))

            # Create the relationship
            if not self.graph.find_relationship(parent_node, parent_node_type, '{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type), relationship_type):
                self.graph.create_relationship(parent_node, parent_node_type, '{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type), relationship_type)
    