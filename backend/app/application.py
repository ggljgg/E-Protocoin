#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import requests
from flask import Flask
from flask_cors import CORS
from .services.console_logger import ConsoleLogger


__all__ = [
    'Application',
]


class Application:
    """ The Application class is a wrapper around several modules.

    Attributes:
        :app (private): The Flask class instance.
        :host (private): The IP address of node on which application runs.
        :port (private): The port of host on which application runs and which
                         uses for connection with peer-to-peer network.
        :wallet (private): The Wallet class instance.
        :block_chain (private): The BlockChain class instance.
        :open_txs (private): The TxList class instance.
        :network (private): The PeerNetwork class instance.
        :instance (private): The Application class instance.
    """

    __instance = None

    #: The reward for miners for creating a new block
    MINING_REWARD = 25.0

    def __init__(self, name, host, port):
        """ The constructor of the Application class. """
        self.__app = Flask(name)
        self.__host = host
        self.__port = port
        self.__wallet = None
        self.__block_chain = None
        self.__open_txs = None
        self.__network = None
        CORS(self.__app, resources=r'/api/*')

    @classmethod
    def get_instance(cls, name=None, host='127.0.0.1', port=None):
        """ Creates and return the class instance.

        Arguments:
            :name: The Flask application context name.
            :host: The IP address of node on which it runs (default is 
                   '127.0.0.1').
            :port: The port of host on which it runs.
        """
        if cls.__instance is None:
            cls.__instance = Application(name, host, port)
        return cls.__instance

    @property
    def port(self):
        """ Returns the port of application. """
        return self.__port

    @property
    def wallet(self):
        """ Returns the wallet of application. """
        return self.__wallet

    @wallet.setter
    def wallet(self, wallet):
        """ Sets the wallet of application. """
        self.__wallet = wallet

    @property
    def block_chain(self):
        """ Returns the block chain of application. """
        return self.__block_chain

    @block_chain.setter
    def block_chain(self, block_chain):
        """ Sets the block chain of application. """
        self.__block_chain = block_chain

    @property
    def open_txs(self):
        """ Returns the open transactions of application. """
        return self.__open_txs

    @open_txs.setter
    def open_txs(self, open_txs):
        """ Sets the open transactions of application. """
        self.__open_txs = open_txs

    @property
    def network(self):
        """ Returns the network of application. """
        return self.__network

    @network.setter
    def network(self, network):
        """ Sets the network of application. """
        self.__network = network

    def register_routes(self, routes, url_prefix=None):
        """ Registers the routes of application. It's the wrapper around Flask
        method \"register_blueprint\".

        Arguments:
            :routes: The list of routes.
            :url_prefix: The url prefix for routes (default is None).
        """
        self.__app.register_blueprint(routes, url_prefix=url_prefix)

    def run(self):
        """ Runs the application on the specified host and port. """
        self.__app.run(host=self.__host, port=self.__port)

    def calculate_balance(self, accountant):
        """ Calls the service which calculates and returns the balance.

        Arguments:
            :accountant: The accountant which calcs balance of participant.
        """
        return accountant.calculate_balance(
            self.__wallet.public_key,
            self.__block_chain,
            self.__open_txs
        )

    def conform_state(self, conformer, block_chain_builder, tx_list_builder):
        """ Calls the service which checks all connected peer nodes' block
        chains, replaces the local one with longer valid ones and returns
        result.

        Arguments:
            :conformer: The application state conformer.
            :block_chain_builder: The block chain builder.
            :tx_list_builder: The transactions list builder.
        """

        replaced, block_chain, open_txs = conformer.conform(
            self.__block_chain,
            self.__open_txs,
            self.__network,
            block_chain_builder,
            tx_list_builder
        )

        if replaced:
            ConsoleLogger.write_log(
                'info',
                __name__,
                'conform_state',
                'The local block chain was replaced because it seems to be '
                'shorter from another block chain.'
            )

            self.__block_chain = block_chain
            self.__open_txs = open_txs
        else:
            ConsoleLogger.write_log(
                'info',
                __name__,
                'conform_state',
                'The local block chain is saved.'
            )

        return replaced
