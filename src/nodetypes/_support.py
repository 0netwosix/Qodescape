# Generate a label looks like "if_line_26", "while_line_26"
# To seperately identify each block (when having multiple "if" in same file)
def generate_block_name_by_line(self, line_number, block_type):
    return ('{block_type}_line_{line_number}'.format(block_type=block_type, line_number=line_number))