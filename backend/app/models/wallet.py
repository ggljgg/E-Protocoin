#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
from Crypto import Random
from ..services.hasher import Hasher
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Wallet:
    """ Creates, loads and holds private and public keys. Manages transaction
    signing and verification.

    Attributes:
        :private_key (private): The private key of wallet.
        :public_key (private): The public key of wallet.
    """

    def __init__(self):
        """ The constructor of the Wallet class. """
        self.__private_key = None
        self.__public_key = None

    @property
    def private_key(self):
        """ Returns the private key of wallet. """
        return self.__private_key

    @property
    def public_key(self):
        """ Returns the public key of wallet. """
        return self.__public_key

    def generate_keys(self):
        """ Generates a new pair of keys. """
        private_key = RSA.generate(2048, Random.new().read)
        public_key = private_key.publickey()

        return (
            binascii
            .hexlify(private_key.exportKey(format='DER'))
            .decode('ascii'),
            binascii
            .hexlify(public_key.exportKey(format='DER'))
            .decode('ascii')
        )

    def assign_keys(self, *args):
        """ Assigns a pair of keys. """
        private_key, public_key = args
        self.__private_key = private_key
        self.__public_key = public_key

    def sign_transaction(self, sender, recipient, amount):
        """ Signs a transaction and return the signature.

        Arguments:
            :sender: The sender of the transaction.
            :recipient: The recipient of the transaction.
            :amount: The amount of coins sent.
        """
        signer = PKCS1_v1_5.new(
            RSA.importKey(
                binascii.unhexlify(self.__private_key)
            )
        )

        data_hash = Hasher.create_data_hash_256(
            sender,
            recipient,
            amount
        )

        signature = signer.sign(data_hash)
        return (binascii
                .hexlify(signature)
                .decode('ascii'))

    def to_dict(self):
        """ Converts a wallet into a serializable dictionary. """
        return {
            'private_key': self.__private_key,
            'public_key': self.__public_key
        }
