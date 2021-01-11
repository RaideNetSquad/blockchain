from time import time
from urllib.parse import urlparse

import json
import hashlib

class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.nodes = set()

        self.new_block(proof = 100, prev_hash = 1)
    
    def new_block(self, proof, prev_hash):
        """
            Создать новый блок в цепи
            :param proof: <int> Доказательство работы алгоритма
            :param previous_hash: <str> Хэш предыдущего блока
            :return: <dict> блок
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'prev_hash': prev_hash or hash(self.chain[-1])
        }

        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
            СОздать транзакцию для перехода к следующему добытому блоку
            :param sender: <str> Адрес отправителя
            :param recipient: <str> Адрес получателя
            :param amount: <int> Количество
            :return: <int> Индекс блока который будет содержать транзакцию
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1
        
    def proof_of_work(self, last_proof):
        '''
            Найти такое число при котором new proof have '0000'
        '''
        proof = 0
        while self.valid_proof(proof, last_proof) is False:
            proof += 1
        return proof

    def valid_proof(self, proof, last_proof):
        '''
            Check == first 4 num hash, от текущего пруфа, 0 
        '''
        encode_str_proof = f'{last_proof}{proof}'.encode()
        hash_proof = hashlib.sha256(encode_str_proof).hexdigest()

        return hash_proof[:4] == "0000"

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.node.add(parsed_url.netloc)

    def valid_chain(self, chain):
        '''
            Проверка валидности цепи, путем обхода каждого блока
        '''
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            if block.prev_hash != self.hash(last_block):
                return False
            
            if not self.valid_proof(block['proof'], last_block['proof']):
                return False
            
            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        '''
        Обходим всех соседей
        if len chain > our and their chain valid (valid_chain)
        replace chain'''
        neighboards = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighboards:
            response = request.get(f'http:/{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        
        if new_chain:
            self.chain = new_chain
            return True
        return False

    @staticmethod
    def hash(block):
        #hashes block
        hashing_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(hashing_string).hexdigest()

    @property
    #must read
    def last_block(self):
        #return the last block in chain
        return self.chain[-1]
