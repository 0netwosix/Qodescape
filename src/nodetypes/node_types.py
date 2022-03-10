from utils import Print

class NodeTypes:
    from nodetypes._expr_array_dim_fetch import expr_array_dim_fetch
    from nodetypes._expr_func_call import expr_func_call
    from nodetypes._expr_include import expr_include
    from nodetypes._expr_method_call import expr_method_call
    from nodetypes._expr_property_fetch import expr_property_fetch_rhs
    from nodetypes._expr_property_fetch import expr_property_fetch_lhs
    from nodetypes._expr_static_call import expr_static_call
    from nodetypes._expr_variable import expr_variable
    from nodetypes._filename_node import filename_node
    from nodetypes._scalar_encapsed import scalar_encapsed
    from nodetypes._stmt_class import stmt_class
    from nodetypes._stmt_class_const import stmt_class_const
    from nodetypes._stmt_class_method import stmt_class_method
    from nodetypes._stmt_echo import stmt_echo
    from nodetypes._stmt_else import stmt_else
    from nodetypes._stmt_else_if import stmt_else_if
    from nodetypes._stmt_expression import stmt_expression
    from nodetypes._stmt_foreach import stmt_foreach
    from nodetypes._stmt_global import stmt_global
    from nodetypes._stmt_if import stmt_if
    from nodetypes._stmt_namespace import stmt_namespace
    from nodetypes._stmt_property import stmt_property
    from nodetypes._stmt_return import stmt_return
    from nodetypes._stmt_use import stmt_use
    from nodetypes._stmt_while import stmt_while
    from nodetypes._support import generate_block_name_by_line

    def __init__(self, graph):
        self.graph = graph    

    def choose_nodetype(self, node, parent_node=None, parent_node_type=None, relationship_type=None, scope=None):
        # Iterate through each key in current node
        for key, value in node.items():
            if key == 'nodeType':
                # Inner HTML
                if value == 'Stmt_InlineHTML':
                    continue