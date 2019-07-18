import hashlib
import json


def hash_string_256(string):
    """ Returns a hash of string. """
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """ Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    hashable_block = block.__dict__.copy()
    # обращение к атрибутам блока зависит от их "скрытости" для внешних интерфейсов
    hashable_block['_Block__transactions'] = [tx.__dict__ for tx in hashable_block['_Block__transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())