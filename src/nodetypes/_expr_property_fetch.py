'''
    Describes a scenario like below
    e.g. $user->password = something();
    e.g. $something = $user->password;

    $user->password
    $user = expr['var']['var']['name']
    password = expr['var']['name']['name']

    1.) Search for "$user" in a variable if not search for a function parameter,
    it should be in one of those. If not it should be an error.
    Once found, "password" is a property of "$user"
    2.) Then search for a relationship "$user -> IS_PROPERTY -> password"
    3.) If not found create the "password" node
    4.) Once created, create the relationship "$something -> ASSIGNS -> password"
'''
def expr_property_fetch(self, expr, parent_node, parent_node_type, scope):
    pass