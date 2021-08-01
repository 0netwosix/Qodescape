# Describes a class method
def stmt_class_method(self, node, parent_node, parent_node_type, relationship_type, scope):
    # Create 'CLASS_METHOD' node
    if not self.graph.find_node(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope)):
        self.graph.create_node(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope))

    # Create 'CLASS_METHOD IS_CLASS_METHOD of Class' relatioship
    if not self.graph.find_relationship(parent_node, parent_node_type, node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), relationship_type):
        self.graph.create_relationship(parent_node, parent_node_type, node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), relationship_type)   

    # Describes method parameters
    if node['params']:
        for param in node['params']:
            if param['var']['nodeType'] == 'Expr_Variable':
                # Create 'PARAM' node
                if not self.graph.find_node(param['var']['name'], '{scope}:{class_method}:PARAM'.format(scope=scope, class_method=node['name']['name'])):
                    self.graph.create_node(param['var']['name'], '{scope}:{class_method}:PARAM'.format(scope=scope, class_method=node['name']['name']))

                # Create 'CLASS_METHOD -> IS_PARAM -> PARAM'
                if not self.graph.find_relationship(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), param['var']['name'], '{scope}:{class_method}:PARAM'.format(scope=scope, class_method=node['name']['name']), 'IS_PARAM'):
                    self.graph.create_relationship(node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), param['var']['name'], '{scope}:{class_method}:PARAM'.format(scope=scope, class_method=node['name']['name']), 'IS_PARAM')

    # Describes the statements inside the method
    if node['stmts']:
        for stmt in node['stmts']:
            if stmt['nodeType'] == 'Stmt_Expression':
                self.stmt_expression(stmt['expr'], node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), '{scope}:{class_method}'.format(scope=scope, class_method=node['name']['name']))
            elif stmt['nodeType'] == 'Stmt_If':
                self.stmt_if(stmt, node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), '{scope}:{class_method}'.format(scope=scope, class_method=node['name']['name']))
            