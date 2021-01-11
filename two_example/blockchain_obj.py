from time import time

import json
import hashlib

class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

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
