from block import Block

import os
import json

def sync():
    '''
        1. reading strings from file
        2. add object to node_blocks
    '''
    node_blocks = []
    #We're assuming that the folder and at least initial block exists
    chaindata_dir = 'chaindata'
    if os.path.exists(chaindata_dir):
        for filename in sorted(os.listdir(chaindata_dir)):
            if filename.endswith('.json'):
                filepath = '%s/%s' % (chaindata_dir, filename)
                print(filepath)
                with open(filepath, 'r') as block_file:
                    block_info = json.load(block_file)
                    block_object = Block(block_info)
                    node_blocks.append(block_object)
    return node_blocks
