#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Transaction:
    """ A transaction which can be added to a block.

    Attributes:
        :sender (private): The sender of coins.
        :recipient (private): The recipient of coins.
        :amount (private): The amount of coins sent.
        :signature (private): The signature of transaction.
    """

    def __init__(self, sender, recipient, amount, signature):
        """ The constructor of the Transaction class. """
        self.__sender = sender
        self.__recipient = recipient
        self.__amount = amount
        self.__signature = signature

    @property
    def sender(self):
        """ Returns the sender of transaction. """
        return self.__sender

    @property
    def recipient(self):
        """ Returns the recipient of transaction. """
        return self.__recipient

    @property
    def amount(self):
        """ Returns the timeamountstamp of transaction. """
        return self.__amount

    @property
    def signature(self):
        """ Returns the signature of transaction. """
        return self.__signature

    def to_dict(self):
        """
        Converts the current transaction into a serializable dictionary.
        """
        return {
            'sender': self.__sender,
            'recipient': self.__recipient,
            'amount': self.__amount,
            'signature': self.__signature
        }
