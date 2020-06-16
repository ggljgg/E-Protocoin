#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from .verifier import Verifier
from .console_logger import ConsoleLogger


class StateConformer:
    """ A class for conforming state of block chain and open transactions
    list. """

    def conform(self, block_chain, open_txs, network,
                block_chain_builder, tx_list_builder):
        """ Checks all connected peer nodes' block chains, replaces the local
        one with longer valid ones and returns result.

        Arguments:
            :block_chain: The local block chain.
            :open_txs: The local open transactions list.
            :network: The local peer network list.
            :block_chain_builder: The block chain builder.
            :tx_list_builder: The transactions list builder.
        """
        winner_block_chain = block_chain
        winner_open_txs = open_txs
        
        replaced = False
        for node in network:
            try:
                node_block_chain = block_chain_builder.build(
                    requests.get(
                        'http://{}/api/v1/block'.format(node.address)
                    ).json()['block chain'],
                    tx_list_builder
                )

                if (node_block_chain.length > winner_block_chain.length and
                    Verifier.verify_chain(node_block_chain)):

                    winner_block_chain = node_block_chain
                    winner_open_txs = tx_list_builder.build(
                        requests.get(
                            'http://{}/api/v1/transaction'
                            .format(node.address)
                        ).json()['open transactions']
                    )

                    replaced = True
            except requests.exceptions.ConnectionError:
                ConsoleLogger.write_log(
                    'error',
                    __name__,
                    'conform',
                    'Resolve conflict was declined because some problems '
                    'with connection on the peer node {} were arised.'
                    .format(node.address)
                )
                continue

        return (
            replaced,
            winner_block_chain,
            winner_open_txs
        )
