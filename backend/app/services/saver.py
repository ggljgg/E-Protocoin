#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from .console_logger import ConsoleLogger


class Saver:
    """ A class for saving application state. """

    @staticmethod
    def save_data(app):
        """ Saves the current application state to a file.

        Arguments:
            :app: The Application class instance.
        """

        prepared_data = (
            app.block_chain.to_list(),
            app.open_txs.to_list(),
            app.network.to_list(),
            app.wallet.to_dict()
        )

        try:
            with open(
                file=r'./app/data/app-{}.dat'.format(app.port),
                mode='w',
                encoding='utf-8'
            ) as f:
                for data in prepared_data:
                    f.write(json.dumps(data))
                    f.write('\n')
            
            ConsoleLogger.write_log(
                'info',
                __name__,
                'save_data',
                'Data saving is done successfully.'
            )

            return True
        except IOError:
            ConsoleLogger.write_log(
                'error',
                __name__,
                'save_data',
                'Data saving is failed.'
            )

            return False
