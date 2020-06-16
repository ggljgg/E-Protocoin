#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from flask import jsonify, request
from ..services.saver import Saver
from ..application import Application
from ..services.verifier import Verifier
from ..models.transaction import Transaction
from ..services.accountant import Accountant
from ..services.console_logger import ConsoleLogger
from ..services.tx_list_builder import TxListBuilder
from ..services.state_conformer import StateConformer
from ..services.block_chain_builder import BlockChainBuilder


__all__ = [
    'get_transactions',
    'create_transaction',
    'broadcast_transaction',
]


def get_transactions():
    app = Application.get_instance()

    if (app.wallet.public_key is None or
        app.wallet.private_key is None):
        response = {
            'message':
            'Getting the open transactions failed '
            'because the wallet is not set up.'
        }
        return (jsonify(response), 401)

    response = {
        'message': 'The open transactions are fetched successfully.',
        'open transactions': app.open_txs.to_list()
    }
    return (jsonify(response), 200)


def create_transaction():
    app = Application.get_instance()

    if (app.wallet.public_key is None or
        app.wallet.private_key is None):
        response = {
            'message':
            'Creating a transaction failed because the wallet is not set up.'
        }
        return (jsonify(response), 401)

    required_fields = ('recipient', 'amount')
    values = request.get_json()

    if not values:
        response = {'message': 'No data found.'}
        return (jsonify(response), 400)
    if not all([field in values for field in required_fields]):
        response = {'message': 'Required data is missing.'}
        return (jsonify(response), 400)

    recipient = values['recipient']
    amount = values['amount']
    signature = app.wallet.sign_transaction(
        app.wallet.public_key,
        recipient,
        amount
    )

    tx = Transaction(
        app.wallet.public_key,
        recipient,
        amount,
        signature
    )

    verified_success = False
    if Verifier.verify_transaction(
        tx,
        Accountant(),
        app.block_chain,
        app.open_txs
    ):
        verified_success = True

    corrupted_block_chain = False
    for node in app.network:
        url = 'http://{}/api/v1/broadcast-transaction'.format(node.address)
        try:
            response = requests.post(url, json={'tx': tx.to_dict()})

            if response.status_code == 401:
                ConsoleLogger.write_log(
                    'info',
                    __name__,
                    'create_transaction',
                    'Transaction was declined because the peer '
                    'node {} not authorized.'.format(node.address)
                )
            elif response.status_code == 409:
                ConsoleLogger.write_log(
                    'warn',
                    __name__,
                    'create_transaction',
                    'Transaction was declined by the node {} because '
                    'conflict resolution is required. The process of '
                    'conform general state was runned.'
                    .format(node.address)
                )

                if not corrupted_block_chain:
                    corrupted_block_chain = app.conform_state(
                        StateConformer(),
                        BlockChainBuilder(),
                        TxListBuilder()
                    )
            elif response.status_code == 400 or response.status_code == 500:
                ConsoleLogger.write_log(
                    'error',
                    __name__,
                    'create_transaction',
                    'Transaction was declined because something went wrong '
                    'on the peer node {}.'.format(node.address)
                )
        except requests.exceptions.ConnectionError:
            ConsoleLogger.write_log(
                'error',
                __name__,
                'create_transaction',
                'Transaction was declined because some problems with '
                'connection on the peer node {} were arised.'
                .format(node.address)
            )
            continue

    if corrupted_block_chain:
        response = {
            'message': 'Creating a transaction via broadcast failed. The '
                       'local block chain was replaced because it was '
                       'corrupted. Try again, please.'
        }
        return (jsonify(response), 200)
    elif verified_success:
        app.open_txs.add_tx(tx)
        Saver.save_data(app)

        response = {
            'message': 'A transaction is added successfully.',
            'transaction': {
                'sender': app.wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': app.calculate_balance(Accountant())
        }
        return (jsonify(response), 201)
    else:
        response = {
            'message': 'Creating a local transaction failed. May be you have '
                       'not coins?'
        }
        return (jsonify(response), 500)


def broadcast_transaction():
    app = Application.get_instance()

    if (app.wallet.public_key is None or
        app.wallet.private_key is None):
        response = {
            'message': 'Reception a broadcastable transaction failed because '
                       'the wallet is not set up.'
        }
        return (jsonify(response), 401)

    values = request.get_json()

    if not values:
        response = {'message': 'No data found.'}
        return (jsonify(response), 400)

    if 'tx' not in values:
        response = {'message': 'Required data is missing.'}
        return (jsonify(response), 400)

    broadcast_tx = values['tx']
    tx = Transaction(
        broadcast_tx['sender'],
        broadcast_tx['recipient'],
        broadcast_tx['amount'],
        broadcast_tx['signature']
    )

    verified_success = False
    if Verifier.verify_transaction(
        tx,
        Accountant(),
        app.block_chain,
        app.open_txs
    ):
        verified_success = True

    message_text = 'A transaction is added successfully.'

    corrupted_block_chain = False
    if app.conform_state(
        StateConformer(),
        BlockChainBuilder(),
        TxListBuilder()
    ):
        corrupted_block_chain = True
        message_text = (
            'A transaction is added successfully, but the local block chain '
            'was replaced because it was corrupted.'
        )

    if verified_success or corrupted_block_chain:
        app.open_txs.add_tx(tx)
        Saver.save_data(app)

        response = {
            'message': message_text,
            'transaction': {
                'sender': broadcast_tx['sender'],
                'recipient': broadcast_tx['recipient'],
                'amount': broadcast_tx['amount'],
                'signature': broadcast_tx['signature']
            }
        }
        return (jsonify(response), 201)
    else:
        response = {
            'message': 'Reception a broadcastable transaction failed '
                       'because the transaction did not pass the '
                       'verification.'
        }
        return (jsonify(response), 409)
