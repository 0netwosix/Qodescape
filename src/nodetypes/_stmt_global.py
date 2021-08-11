'''
    Describes a global variables in a file. 
    Functionality - imports variables from the global scope into the local scope.

    e.g. global $GVAR;
    
    HOW IT WORKS!
    1.) I creates "GVAR" node with folowing labels if it does not exist.
        - scope = CLASS.name, CLASS_METHOD.name or FILENAME.name
        - GLOBAL_VARIABLE
    2.) Then it creates the following relationship if it does not exist.
        - relationship_types = IS_GLOBAL_VARIABLE
        - (parent_node)-[IS_GLOBAL_VARIABLE]->(GVAR:{scope:GLOBAL_VARIABLE})
'''
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
