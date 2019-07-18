from time import time
from utility.printable import Printable

class Block(Printable):
    """ """

    def __init__(self, index, previous_hash, transactions, proof, timestamp=time()):
        self.__index = index
        self.__previous_hash = previous_hash
        self.__transactions = transactions
        self.__proof = proof
        self.__timestamp = timestamp
    
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
