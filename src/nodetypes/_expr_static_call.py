'''
    Describes a static call.

    e.g. self::__construct();
'''
def expr_static_call(self, name, parent_node, parent_node_type, scope):
    if name['nodeType'] == 'Identifier':       
        # Child class will also be a Method in this case
        # Therefore it's scope can be taken as (scope-parent_node)
        pass