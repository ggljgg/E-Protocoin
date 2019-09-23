import json
import hashlib


def hash_string_256(string):
    """ Returns a hash of string.
    
    Arguments:
        :string: ...
    """
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """ Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    return hash_string_256(
        json.dumps(
            block.to_dict(),
            sort_keys=True
        ).encode()
    )