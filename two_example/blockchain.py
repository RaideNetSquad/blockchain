'''
    Объект блокчейна
    1. Создаем список (для хранения цепочек блоков)
'''
from uuid import uuid4
from flask import Flask, jsonify, request

from blockchain_obj import BlockChain

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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)