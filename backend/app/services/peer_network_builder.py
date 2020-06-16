#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..models.node import Node
from ..models.peer_network import PeerNetwork


class PeerNetworkBuilder:
    """ A class for building the peer network. """

    def build(self, network):
        """ Creates the peer network nodes from list.

        Arguments:
            :network: The list of peer nodes.
        """
        return PeerNetwork({self.__build_node(node) for node in network})

    def __build_node(self, node):
        """ Creates a node from dictionary.

        Arguments:
            :node: The dictionary of node with info.
        """
        return Node(node['address'])
