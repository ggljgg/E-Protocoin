from time import time

class Block:
    """ """

    def __init__(self, index, previous_hash, transactions, proof, timestamp=time()):
        self.__index = index
        self.__previous_hash = previous_hash
        self.__transactions = transactions
        self.__proof = proof
        self.__timestamp = timestamp

    def __str__(self):
        return ('index: {0}\n'
                'previous hash: {1}\n'
                'proof: {2}\n'
                'timestamp: {3}\n'
                'transactions: {4}'
                ).format(
                    self.__index,
                    self.__previous_hash,
                    self.__proof,
                    self.__timestamp,
                    self.__transactions
                )

    def __repr__(self):
        return str({
            'index': self.__index,
            'previous hash': self.__previous_hash,
            'proof': self.__proof,
            'timestamp': self.__timestamp,
            'transactions': self.__transactions
        })

    @property
    def index(self):
        return self.__index

    @property
    def previous_hash(self):
        return self.__previous_hash

    @property
    def transactions(self):
        return self.__transactions

    @property
    def proof(self):
        return self.__proof

    @property
    def timestamp(self):
        return self.__timestamp

    def to_dict(self):
        return {
            'index': self.__index,
            'previous hash': self.__previous_hash,
            'proof': self.__proof,
            'timestamp': self.__timestamp,
            'transactions': [tx.to_dict() for tx in self.__transactions]
        }
