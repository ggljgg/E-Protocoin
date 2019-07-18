from time import time

class Block:
    """ """
    # __slots__ = ('__index', '__previous_hash', '__transactions', '__proof', '__timestamp')

    def __init__(self, index, previous_hash, transactions, proof, time=time()):
        self.__index = index
        self.__previous_hash = previous_hash
        self.__transactions = transactions
        self.__proof = proof
        self.__timestamp = time
    
    @property
    def previous_hash(self):
        return self.__previous_hash

    @property
    def transactions(self):
        return self.__transactions

    @property
    def proof(self):
        return self.__proof
