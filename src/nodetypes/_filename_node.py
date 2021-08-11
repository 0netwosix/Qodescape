'''
    Create a node for the File name.
    Filename or Namespace would be the root node for each file.  

    e.g. test.php

    HOW IT WORKS!
    1.) It creates "test" node with following labels if it is not there already.
        - FILENAME
    - This is the very first node that it creates if there is no "namespace" statement in the file.
    - Therefore no scope labels are added to this node. Only label would be "FILENAME".
    - Every statement that falls outside the "CLASS", is a direct child of this node.
'''
def filename_node(self, file_name):
    # Create 'FILENAME' node
    if not self.graph.find_node(file_name, 'FILENAME'):
        # Print.clear_print('File_Name Node -> {file_name}'.format(file_name=file_name))
        self.graph.create_node(file_name, 'FILENAME')