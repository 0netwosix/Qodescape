'''
    Generate a custom name like below. 
    Helps to uniquley identify each IF, WHILE blocks when one file has multiple of those.

    e.g. IF_line_26, ELSEIF_line_26, ELSE_line_26, WHILE_line_26
'''
def generate_block_name_by_line(self, line_number, block_type):
    return ('{block_type}_line_{line_number}'.format(block_type=block_type, line_number=line_number))