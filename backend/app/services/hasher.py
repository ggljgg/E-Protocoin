#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from Crypto.Hash import MD5
from Crypto.Hash import SHA256


class Hasher:
    """ A helper class which offer various static and class-based
    hash methods. """

    @classmethod
    def __new__(cls):
        raise TypeError('Hasher is a static class.')

    @staticmethod
    def hash_string_md5(string):
        """ Creates a MD5 hash for a given input string.

        Arguments:
            :string: The string which should be hashed.
        """
        return MD5.new(string.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_string_256(string):
        """ Creates a SHA256 hash for a given input string.

        Arguments:
            :string: The string which should be hashed.
        """
        return SHA256.new(string.encode('utf-8'))

    @classmethod
    def hash_block(cls, block):
        """ Hashes a block and returns a string representation of it.

        Arguments:
            :block: The block that should be hashed.
        """
        return cls.hash_string_256(
            json.dumps(
                block.to_dict(),
                sort_keys=True
            )
        ).hexdigest()

    @classmethod
    def create_data_hash_256(cls, sender, recipient, amount):
        """ Hashes a transaction data and returns a string representation
        of it.

        Arguments:
            :sender: The sender of the transaction.
            :recipient: The recipient of the transaction.
            :amount: The amount of coins sent.
        """
        return cls.hash_string_256(
            (
                str(sender) +
                str(recipient) +
                str(amount)
            )
        )
