#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..models.block import Block
from ..models.block_chain import BlockChain


class BlockChainBuilder:
    """ A class for building the block chain. """

    def build(self, block_chain, tx_list_builder):
        """ Creates a block chain from list.

        Arguments:
            :block_chain: The list of blocks.
        """
        return BlockChain([
            self.__build_block(block, tx_list_builder) for block in block_chain
        ])

    def __build_block(self, block, tx_list_builder):
        """ Creates a block from dictionary.

        Arguments:
            :block: The dictionary of block with info.
            :tx_list_builder: The transactions list builder.
        """
        return Block(
            block['index'],
            block['previous_hash'],
            tx_list_builder.build(block['transactions']),
            block['proof'],
            block['timestamp']
        )
