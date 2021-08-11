'''
    Describes $_GET[], $_POST[], $_REQUEST[] like statements.

    e.g. $_GET['product']

    HOW IT WORKS!
    1.) It checks whether the "array_type" is "_GET" or "_REQUEST", if so it proceeds.
    2.) Then it checks whether the type of the variable inside $_GET[] is a "Scalar_String" (constnat), if so it proceeds.
    3.) Then it contructs the node name "SCALAR_product" and checks whether it is available with following labels.
        - scope         = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - array_type    = _GET, _REQUEST
        - VARIABLE
        3.1.) If not it creates the node "SCALAR_product" with above labels.
            - SCALAR_product:{scope:array_type:VARIABLE}
    4.) Then it creates the following relationship if it does not exist.
        - relationship_types = ASSIGNS, IS_ARGUMENT
        - (parent_node)-[relationship_type]->(SCALAR_product:{scope:array_type:VARIABLE})
'''
def expr_array_dim_fetch(self, expr, parent_node, parent_node_type, relationship_type, scope, array_type):
    if array_type == '_GET' or array_type == '_REQUEST': 
        if expr['dim']['nodeType'] == 'Scalar_String':
            # Create the node
            if not self.graph.find_node('{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type)):
                self.graph.create_node('{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type))

            # Create the relationship
            if not self.graph.find_relationship(parent_node, parent_node_type, '{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type), relationship_type):
                self.graph.create_relationship(parent_node, parent_node_type, '{keyword}{variable_name}'.format(keyword='SCALAR_', variable_name=expr['dim']['value']), '{scope}:{array_type}:VARIABLE'.format(scope=scope, array_type=array_type), relationship_type)
    