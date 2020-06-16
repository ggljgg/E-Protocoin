#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
from .hasher import Hasher
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from .console_logger import ConsoleLogger


class Verifier:
    """ A helper class which offer various static and class-based verification
    and validation methods. """

    @classmethod
    def __new__(cls):
        raise TypeError('Verifier is a static class.')

    @classmethod
    def verify_chain(cls, block_chain):
        """ Verifies the current block chain and return True if it's valid,
        False otherwise.

        Arguments:
            :block_chain: The block chain.
        """
        for (index, block) in enumerate(block_chain):
            if index == 0:
                continue

            if block.previous_hash != Hasher.hash_block(block_chain[index - 1]):
                ConsoleLogger.write_log(
                    'warn',
                    __name__,
                    'verify_chain',
                    'Block chain is invalid.'
                )

                return False

            if not cls.valid_proof(
                block.transactions[:-1],
                block.previous_hash,
                block.proof
            ):
                ConsoleLogger.write_log(
                    'warn',
                    __name__,
                    'verify_chain',
                    'Proof of work is invalid.'
                )

                return False
        return True

    @staticmethod
    def valid_proof(tx_list, last_hash, proof):
        """ Checks that the proof (nonce) is correctly guessed.

        Arguments:
            :tx_list: The transactions list which was included in the block.
            :last_hash: The hash of the previous block in the block chain.
            :proof (nonce): A random integer number.
        """
        guess = (
            str([tx.to_dict() for tx in tx_list]) +
            str(last_hash) +
            str(proof)
        )
        return (Hasher
                .hash_string_256(guess)
                .hexdigest()[0:2] == '00')

    @classmethod
    def verify_transactions(cls, tx_list, accountant, block_chain):
        """ Verifies the all open transactions.

        Arguments:
            :tx_list: The transactions list.
            :accountant: The accountant for calcs balance.
            :block_chain: The block chain.
        """
        return all(
            [
                cls.verify_transaction(
                    tx,
                    accountant,
                    block_chain,
                    tx_list,
                    False
                ) for tx in tx_list
            ]
        )

    @classmethod
    def verify_transaction(cls, tx, accountant, block_chain, tx_list, check_funds=True):
        """ Verifies a current transaction.

        Arguments:
            :tx: The transaction that should be verified.
            :accountant: The accountant for calcs balance.
            :block_chain: The block chain.
            :tx_list: The transactions list.
            :check_funds: The flag of checking funds (default = True).
        """
        if check_funds:
            return (
                accountant.calculate_balance(tx.sender, block_chain, tx_list) >=
                tx.amount and cls.verify_tx_signature(tx)
            )
        else:
            return cls.verify_tx_signature(tx)

    @staticmethod
    def verify_tx_signature(tx):
        """ Verifies the signature of transaction.

        Arguments:
            :tx: The transaction that should be verified.
        """
        public_key = RSA.importKey(
            binascii.unhexlify(tx.sender)
        )

        verifier = PKCS1_v1_5.new(public_key)

        data_hash = Hasher.create_data_hash_256(
            tx.sender,
            tx.recipient,
            tx.amount
        )

        return verifier.verify(
            data_hash,
            binascii.unhexlify(tx.signature)
        )
