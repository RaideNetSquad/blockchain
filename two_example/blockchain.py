'''
    Объект блокчейна
    1. Создаем список (для хранения цепочек блоков)
'''
from uuid import uuid4
from flask import Flask, jsonify, request

from blockchain_obj import BlockChain

from multiprocessing import Process

app = Flask(__name__)

#gen id for address
node_identifier = str(uuid4()).replace('-', '')

blockChain = BlockChain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockChain.last_block
    last_proof = last_block['proof']

    proof = blockChain.proof_of_work(last_proof)
    #if sender 0 - have new coin
    blockChain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    prev_hash = blockChain.hash(last_block)
    block = blockChain.new_block(proof, prev_hash)

    res = {
        'index': block['index'],
        'timestamp': block['timestamp'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'prev_hash': block['prev_hash']
    }
    return jsonify(res), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    '''
    {
        "sender": "my address",
        "recipient": "someone else's address",
        "amount": 5
    }
    '''
    values = request.get_json()

    #fields data from request
    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing values', 400
    
    #create new trasaction
    index = blockChain.new_transaction(values['sender'], values['recipient'], values['amount'])
    
    res = {
            'message': f'transaction will be added to block {index}'
    }

    return res, 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockChain.chain,
        'len': len(blockChain.chain)
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    
    for node in nodes:
        blockChain.register_node(node)
    
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockChain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockChain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockChain.chain
        }

    return jsonify(response), 200

def app_f():
    app.run(host='127.0.0.1', port=5000)

def app_f1():
    app.run(host='127.0.0.1', port=5001)

if __name__ == '__main__':
    
    process1 = Process(target=app_f)
    process2 = Process(target=app_f1)

    process1.start()
    process2.start()
