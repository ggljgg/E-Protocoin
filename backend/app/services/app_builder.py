#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..models.wallet import Wallet
from ..models.tx_list import TxList
from ..application import Application
from .tx_list_builder import TxListBuilder
from ..models.block_chain import BlockChain
from ..models.peer_network import PeerNetwork
from .block_chain_builder import BlockChainBuilder
from .peer_network_builder import PeerNetworkBuilder


class AppBuilder:
    """ A class for building the application.
    
    Attributes:
        :app (private): The Application class instance.
    """

    def __init__(self, name, port):
        """ The constructor of the AppBuilder class. """
        self.__app = Application.get_instance(name, port=port)

    def build(self, *args):
        """ Builds and returns the Application class instance. """

        wallet_data = args[3]
        network_data = args[2]
        open_txs_data = args[1]
        block_chain_data = args[0]

        self.__build_wallet(wallet_data)
        self.__build_network(network_data, PeerNetworkBuilder())
        self.__build_open_txs(open_txs_data, TxListBuilder())
        self.__build_block_chain(
            block_chain_data,
            BlockChainBuilder(),
            TxListBuilder()
        )

        return self.__app

    def __build_wallet(self, data):
        """ Builds the application wallet.

        Arguments:
            :data: The data for building.
        """
        if not data:
            self.__app.wallet = Wallet()
        else:
            self.__app.wallet = Wallet()
            self.__app.wallet.assign_keys(
                data['private_key'],
                data['public_key']
            )

    def __build_network(self, data, network_builder):
        """ Builds the application network.

        Arguments:
            :data: The data for building.
            :network_builder: The network builder.
        """
        if not data:
            self.__app.network = PeerNetwork()
        else:
            self.__app.network = network_builder.build(data)

    def __build_open_txs(self, data, tx_list_builder):
        """ Builds the application open transactins list.

        Arguments:
            :data: The data for building.
            :tx_list_builder: The transactions list builder.
        """
        if not data:
            self.__app.open_txs = TxList()
        else:
            self.__app.open_txs = tx_list_builder.build(data)

    def __build_block_chain(self, data, block_chain_builder, tx_list_builder):
        """ Builds the application block chain.

        Arguments:
            :data: The data for building.
            :block_chain_builder: The block chain builder.
            :tx_list_builder: The transactions list builder.
        """
        if not data:
            self.__app.block_chain = BlockChain()
        else:
            self.__app.block_chain = block_chain_builder.build(
                data,
                tx_list_builder
            )
