#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Node:
    """ A peer node which can be added to the peer network.

    Attributes:
        :address (private): The IP address of peer node.
    """

    def __init__(self, address):
        """ The constructor of the PeerNode class. """
        self.__address = address

    @property
    def address(self):
        """ Returns the IP address of peer node. """
        return self.__address

    def to_dict(self):
        """ Converts a peer node into a serializable dictionary. """
        return {
            'address': self.__address
        }
