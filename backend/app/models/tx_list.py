#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class TxList:
    """ The TxList class manages the list of transactions.

    Attributes:
        :data (private): The list of transactions.
    """

    def __init__(self, data_list=None):
        """ The constructor of the TxList class. """
        self.__data = data_list or []

    def __iter__(self):
        """ Returns iterator for container. """
        for item in self.__data:
            yield item

    def __getitem__(self, index):
        """
        Returns a transaction or part of the transactions list by index.
        """
        return self.__data[index]

    def add_tx(self, tx):
        """ Adds a transaction to the transaction list.

        Arguments:
            :tx: The transaction that should be added.
        """
        self.__data.append(tx)

    def remove_tx(self, tx):
        """ Removes a transaction from the transaction list.

        Arguments:
            :tx: The transaction that should be added.
        """
        self.__data.remove(tx)

    def clear(self):
        """ Clears the transaction list. """
        self.__data.clear()

    def copy(self):
        """ Creates a new copy of transaction list. """
        return TxList([item for item in self.__data])

    def to_list(self):
        """ Converts the current tx list into a serializable list. """
        return [tx.to_dict() for tx in self.__data]
