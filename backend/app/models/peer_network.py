#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..services.hasher import Hasher


class PeerNetwork:
    """ A peer network which storage all nodes.

    Attributes:
        :data (private): The set of all connected peer nodes.
    """

    def __init__(self, data_set=None):
        """ The constructor of the PeerNetwork class. """
        self.__data = data_set or set()

    def __iter__(self):
        """ Returns iterator for container. """
        for item in self.__data:
            yield item

    def add_node(self, node):
        """ Adds a new node to the peer nodes set and saves data.

        Arguments:
            :node: The node which should be added.
        """
        if not any(
            [self.__compare_strings_hashes(
                node.address,
                item['address']
            ) for item in self.to_list()]
        ):
            self.__data.add(node)

    def remove_node(self, address):
        """ Removes a node from the peer nodes set and saves data.

        Arguments:
            :address: The node address which should be removed.
        """
        node_reference = None
        for node in self.__data:
            if self.__compare_strings_hashes(address, node.address):
                node_reference = node
                break
        
        self.__data.discard(node_reference)

    def to_list(self):
        """ Converts the current peer network into a serializable list. """
        return [node.to_dict() for node in self.__data]

    def __compare_strings_hashes(self, string_1, string_2):
        """ Compares two hashes of strings and returns the result.

        Arguments:
            :string_1: The string class instance.
            :string_2: The string class instance.
        """
        return (
            Hasher.hash_string_md5(string_1)
            == Hasher.hash_string_md5(string_2)
        )
