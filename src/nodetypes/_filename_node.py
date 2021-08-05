# Create a node for the FileName
def filename_node(self, file_name):
    # Create 'FILENAME' node
    if not self.graph.find_node(file_name, 'FILENAME'):
        # Print.clear_print('File_Name Node -> {file_name}'.format(file_name=file_name))
        self.graph.create_node(file_name, 'FILENAME')