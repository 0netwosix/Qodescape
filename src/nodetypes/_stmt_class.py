# Describes "class ClassName extends AnotherClass implements SomeOtherClass"
def stmt_class(self, node, parent_node, parent_node_type, relationship_type, scope):
    # Labels that denote the scope of the class
    stmt_class_type = '{scope}:CLASS'.format(scope=scope)

    if node['name']['nodeType'] == 'Identifier':
        # Create 'CLASS' node
        if not self.graph.find_node(node['name']['name'], 'CLASS'):
            self.graph.create_node(node['name']['name'], 'CLASS')

        # Create 'Namespace CONTAINS Class' relationship
        if not self.graph.find_relationship(parent_node, parent_node_type, node['name']['name'], 'CLASS', relationship_type):
            self.graph.create_relationship(parent_node, parent_node_type, node['name']['name'], 'CLASS', relationship_type)  

    # If class contains "extends"
    if node['extends']:
        # Create extended 'CLASS' node
        if not self.graph.find_node('\\'.join(node['extends']['parts']), 'CLASS'):
            self.graph.create_node('\\'.join(node['extends']['parts']), 'CLASS')

        # Create 'Class EXTENDS AnotherClass' relationship
        if not self.graph.find_relationship(node['name']['name'], 'CLASS', '\\'.join(node['extends']['parts']), 'CLASS', 'EXTENDS'):
            self.graph.create_relationship(node['name']['name'], 'CLASS', '\\'.join(node['extends']['parts']), 'CLASS', 'EXTENDS')   

    # If class contains "implements"
    if node['implements']:
        for interface in node['implements']:
            # Create implemented 'CLASS' node
            if not self.graph.find_node('\\'.join(interface['parts']), 'CLASS'):
                self.graph.create_node('\\'.join(interface['parts']), 'CLASS')

            # Create 'Class IMPLEMENTS AnotherClass' relationship
            if not self.graph.find_relationship(node['name']['name'], 'CLASS', '\\'.join(interface['parts']), 'CLASS', 'IMPLEMENTS'):
                self.graph.create_relationship(node['name']['name'], 'CLASS', '\\'.join(interface['parts']), 'CLASS', 'IMPLEMENTS')     

    # Deal with "stmt"s inside the class
    if node['stmts']:
        # "statement" represents each line inside the class
        for statement in node['stmts']:
            if statement['nodeType'] == 'Stmt_ClassMethod':
                self.stmt_class_method(statement, node['name']['name'], 'CLASS', 'IS_CLASS_METHOD', node['name']['name'])
            elif statement['nodeType'] == 'Stmt_ClassConst':
                self.stmt_class_const(statement['consts'], node['name']['name'], 'CLASS', node['name']['name'])
            elif statement['nodeType'] == 'Stmt_Property':
                self.stmt_property(statement['props'], node['name']['name'], 'CLASS', node['name']['name'])
