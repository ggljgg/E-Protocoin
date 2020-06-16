#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..models.tx_list import TxList
from ..models.transaction import Transaction


class TxListBuilder:
    """ A class for building the transactions list. """

    def build(self, tx_list):
        """ Creates a transactions list from list. 

        Arguments:
            :tx_list: The list of transactions.
        """
        return TxList([self.__build_tx(tx) for tx in tx_list])

    def __build_tx(self, tx):
        """ Creates a transaction from dictionary.

        Arguments:
            :tx: The dictionary of transaction with info.
        """
        return Transaction(
            tx['sender'],
            tx['recipient'],
            tx['amount'],
            tx['signature']
        )
