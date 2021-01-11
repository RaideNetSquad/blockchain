from flask import Flask
from block import Block

import sync

import os
import json

node = Flask(__name__)

node_block = sync.sync()

@node.route('/blockchain.json', methods=['GET'])

def blockchain():

    node_blocks = sync.sync()
    python_blocks = []

    for block in node_blocks:
        python_blocks.append(block.__dict__())

    json_blocks = json.dumps(python_blocks)

    return json_blocks

if  __name__ == '__main__':
    node.run()