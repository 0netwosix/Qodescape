class NodeType:
    from nodetypes._expr_array_dim_fetch import expr_array_dim_fetch
    from nodetypes._expr_func_call import expr_func_call
    from nodetypes._expr_variable import expr_variable
    from nodetypes._filename_node import filename_node
    from nodetypes._scalar_encapsed import scalar_encapsed
    from nodetypes._stmt_class import stmt_class
    from nodetypes._stmt_class_const import stmt_class_const
    from nodetypes._stmt_class_method import stmt_class_method
    from nodetypes._stmt_echo import stmt_echo
    from nodetypes._stmt_else import stmt_else
    from nodetypes._stmt_expression import stmt_expression
    from nodetypes._stmt_global import stmt_global
    from nodetypes._stmt_if import stmt_if
    from nodetypes._stmt_namespace import stmt_namespace
    from nodetypes._stmt_property import stmt_property
    from nodetypes._stmt_while import stmt_while
    from nodetypes._support import generate_block_name_by_line

    def __init__(self, graph):
        self.graph = graph       