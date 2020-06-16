#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .block import Block
from .tx_list import TxList


class BlockChain:
    """ The BlockChain class manages the chain of blocks.

    Attributes:
        :data (private): The list of blocks.
    """

    def __init__(self, data_list=None):
        """ The constructor of the BlockChain class. """
        genesis_block = Block(0, '', TxList(), 100)
        self.__data = data_list or [genesis_block]

    def __iter__(self):
        """ Returns iterator for container. """
        for item in self.__data:
            yield item

    def __getitem__(self, index):
        """ Returns a block or part of the block chain by index. """
        return self.__data[index]

    @property
    def last_block(self):
        """ Returns a last block of the block chain. """
        if self.length > 0:
            return self.__data[-1]

    @property
    def length(self):
        """ Returns a length of the block chain. """
        return len(self.__data)

    def add_block(self, block):
        """ Adds a block to the block chain. """
        self.__data.append(block)

    def to_list(self):
        """ Converts the block chain into a serializable list. """
        return [block.to_dict() for block in self.__data]
