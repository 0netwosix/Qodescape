from utils.support import Print

# Describes a If block
def stmt_if(self, slice, parent_node, parent_node_type, scope):
    if slice['cond']['attributes']['startLine']:
        if_node_type = '{scope}:IF'.format(scope=scope)
        if_node_name = self.generate_block_name_by_line(slice['cond']['attributes']['startLine'], 'IF')

        # Create If block node
        if not self.graph.find_node(if_node_name, if_node_type):
            self.graph.create_node(if_node_name, if_node_type)

        # Create If_block relationship with parent
        if not self.graph.find_relationship(parent_node, parent_node_type, if_node_name, if_node_type, 'IF_BLOCK'):
            self.graph.create_relationship(parent_node, parent_node_type, if_node_name, if_node_type, 'IF_BLOCK')

        # Describes statements inside the IF block
        if slice['stmts']:
            for stmt in slice['stmts']:
                # If the statement is a While block
                if stmt['nodeType'] == 'Stmt_While':
                    self.stmt_while(stmt, if_node_name, if_node_type, '{this_node}:{parent_scope}'.format(this_node=if_node_name, parent_scope=parent_node))

        # Describes the Else block
        if slice['else']:
            if slice['else']['nodeType'] == 'Stmt_Else':
                self.stmt_else(slice['else'], if_node_name, if_node_type, '{this_node}:{parent_scope}'.format(this_node=if_node_name, parent_scope=parent_node))
    
        # Describes the ELSE IF block
        if slice['elseifs']:
            pass
    
    else:
        Print.error_print('[ERROR]', 'Issue in "If[conditions][attributes]"')