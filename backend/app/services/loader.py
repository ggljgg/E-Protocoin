#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from .console_logger import ConsoleLogger


class Loader:
    """ A class for loading application state. """

    @staticmethod
    def load_data(port):
        """ Loads an application data from a file.

        Arguments:
            :port: The port of host on which application will be run.
        """
        try:
            with open(
                file=r'./app/data/app-{}.dat'.format(port),
                mode='r',
                encoding='utf-8'
            ) as f:
                file_content = f.readlines()

                block_chain = json.loads(file_content[0][:-1])
                open_txs = json.loads(file_content[1][:-1])
                network = json.loads(file_content[2][:-1])
                wallet = json.loads(file_content[3][:-1])

            ConsoleLogger.write_log(
                'info',
                __name__,
                'load_data',
                'Data uploaded successfully.'
            )

            return (
                block_chain,
                open_txs,
                network,
                wallet,
            )
        except (IOError, IndexError):
            ConsoleLogger.write_log(
                'error',
                __name__,
                'load_data',
                'No data was uploaded because the data file was not found.'
            )

            return (
                False,
                False,
                False,
                False,
            )
