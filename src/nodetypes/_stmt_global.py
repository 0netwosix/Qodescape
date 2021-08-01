# Describes a global variables in a file. 
# e.g. "global $CFG;"
def stmt_global(self, vars, parent_node, parent_node_type, scope):
    # nodeType          -> GLOBAL_VARIABLE
    # relationshipType  -> IS_GLOBAL_VARIABLE
    if vars:
        for var in vars:
            if var['nodeType'] == 'Expr_Variable':
                # Create 'GLOBAL_VARIABLE' node
                if not self.graph.find_node(var['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope)):
                    self.graph.create_node(var['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope))

                # Create 'Filename -> IS_GLOBAL_VARIABLE -> GLOBAL_VARIABLE'
                if not self.graph.find_relationship(parent_node, parent_node_type, var['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope), 'IS_GLOBAL_VARIABLE'):
                    self.graph.create_relationship(parent_node, parent_node_type, var['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope), 'IS_GLOBAL_VARIABLE')
