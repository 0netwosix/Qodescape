'''
    Describes a class method.

    e.g. public function update($id, $name)

    TODO: 
        1. Call a generalized function to map nodes in stmts.

    HOW IT WORKS!
    1.) It creates "update" node with following labels if it is not already there.
        - scope = CLASS.name or FILENAME.name
        - CLASS_METHOD
    2.) Then it creates the following realtionship if it is not already there.
        - relationship_types = IS_CLASS_METHOD
        - (parent_node)-[IS_CLASS_METHOD]->(update:{scope:CLASS_METHOD})
    3.) Then it checks whether it has parameters, if yes,
        3.1.) It loops through each parameter and creates "id" and "name" nodes with following labels if they are not already there.
            - scope = CLASS.name or FILENAME.name
            - CLASS_METHOD.name
            - PARAM
        3.2.) Then it creates the following relationship with each of them if they are not already there.
            - (parent_node)-[IS_PARAM]->(id:{scope:CLASS_METHOD.name:PARAM})
    4.) Once done, it looks at statements inside the method and based on that nodeType it'll call relevant nodeType method.
        - If it is a "Stmt_If", it'll call "stmt_if()"
        - If it is a "Stmt_Expression" it'll call "stmt_expression()"
        - ...
'''
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
            if stmt['nodeType'] == 'Stmt_Global':
                self.stmt_global(stmt['vars'], node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), '{scope}:{class_method}'.format(scope=scope, class_method=node['name']['name']))
            elif stmt['nodeType'] == 'Stmt_Expression':
                self.stmt_expression(stmt['expr'], node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), '{scope}:{class_method}'.format(scope=scope, class_method=node['name']['name']))
            elif stmt['nodeType'] == 'Stmt_If':
                self.stmt_if(stmt, node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), '{scope}:{class_method}'.format(scope=scope, class_method=node['name']['name']))
            elif stmt['nodeType'] == 'Stmt_Return':
                self.stmt_return(stmt['expr'], node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), '{scope}:{class_method}'.format(scope=scope, class_method=node['name']['name']))
            elif stmt['nodeType'] == 'Stmt_Echo':
                self.stmt_echo(stmt['exprs'], node['name']['name'], '{scope}:CLASS_METHOD'.format(scope=scope), '{scope}:{class_method}'.format(scope=scope, class_method=node['name']['name']))