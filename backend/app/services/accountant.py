#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools


class Accountant:
    """ A class for calculating the funds. """

    def calculate_balance(self, participant, block_chain, open_txs):
        """ Calculates and returns the participant's balance. 

        Arguments:
            :participant: The public key as unique participant id.
            :block_chain: The block chain.
            :open_txs: The open transactions list.
        """
        tx_sender = self.__form_amounts_lists_list('sender', participant, block_chain)
        open_tx_sender = self.__form_amounts_list(
            'sender',
            participant,
            open_txs
        )

        tx_sender.append(open_tx_sender)
        tx_recipient = self.__form_amounts_lists_list(
            'recipient',
            participant,
            block_chain
        )

        amount_sent = self.__calc_general_amount(tx_sender)
        amount_received = self.__calc_general_amount(tx_recipient)

        return amount_received - amount_sent

    def __form_amounts_lists_list(self, role, participant, block_chain):
        """ Forms a transaction list of participant for determined role from
        current block chain. 

        Arguments:
            :role: The role in the transaction.
            :participant: The public key as unique participant id.
            :block_chain: The block chain.
        """
        return [
            self.__form_amounts_list(role, participant, block.transactions)
            for block in block_chain
        ]

    def __form_amounts_list(self, role, participant, tx_list):
        """ Forms the amounts list of participant for determined role and
        transaction list from current block chain. 

        Arguments:
            :role: The role in the transaction.
            :participant: The public key as unique participant id.
            :tx_list: The transactions list.
        """
        amount_list = []
        for tx in tx_list:
            if role == 'sender' and tx.sender == participant:
                amount_list.append(tx.amount)
            if role == 'recipient' and tx.recipient == participant:
                amount_list.append(tx.amount)
        return amount_list

    def __calc_general_amount(self, amounts_list):
        """ Calcs the general amount from the amounts list. 

        Arguments:
            :amounts_list: The list of amounts.
        """
        return functools.reduce(
            lambda tx_sum, tx_amt:
                tx_sum + sum(tx_amt)
                if len(tx_amt) > 0
                else tx_sum,
            amounts_list,
            0
        )
