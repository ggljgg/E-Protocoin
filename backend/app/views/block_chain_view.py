#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from ..models.block import Block
from flask import jsonify, request
from ..services.saver import Saver
from ..services.hasher import Hasher
from ..application import Application
from ..services.verifier import Verifier
from ..models.transaction import Transaction
from ..services.accountant import Accountant
from ..services.console_logger import ConsoleLogger
from ..services.tx_list_builder import TxListBuilder
from ..services.state_conformer import StateConformer
from ..services.block_chain_builder import BlockChainBuilder


__all__ = [
    'get_blocks',
    'create_block',
    'broadcast_block',
]


def get_blocks():
    app = Application.get_instance()

    if (app.wallet.public_key is None or
        app.wallet.private_key is None):
        response = {
            'message':
            'Getting the block chain failed because the wallet is not set up.'
        }
        return (jsonify(response), 401)

    response = {
        'message': 'The block chain is fetched successfully.',
        'block chain': app.block_chain.to_list()
    }
    return (jsonify(response), 200)


def create_block():
    app = Application.get_instance()

    if (app.wallet.public_key is None or
        app.wallet.private_key is None):
        response = {
            'message':
            'Creating a block failed because the wallet is not set up.'
        }
        return (jsonify(response), 401)

    last_hash = Hasher.hash_block(app.block_chain.last_block)

    # Searches a proof of work
    proof = 0
    while not Verifier.valid_proof(
        app.open_txs,
        last_hash,
        proof
    ):
        proof += 1

    reward_tx = Transaction(
        'REWARDING SYSTEM',
        app.wallet.public_key,
        app.MINING_REWARD,
        ''
    )

    copied_transactions = app.open_txs.copy()

    verified_success = False
    if Verifier.verify_transactions(
        copied_transactions,
        Accountant(),
        app.block_chain
    ):
        verified_success = True

    copied_transactions.add_tx(reward_tx)
    block = Block(
        app.block_chain.length,
        last_hash,
        copied_transactions,
        proof
    )

    corrupted_block_chain = False
    for node in app.network:
        url = 'http://{}/api/v1/broadcast-block'.format(node.address)
        try:
            response = requests.post(url, json={'block': block.to_dict()})
            
            if response.status_code == 401:
                ConsoleLogger.write_log(
                    'info',
                    __name__,
                    'create_block',
                    'Block was declined because the peer node {} not '
                    'authorized.'.format(node.address)
                )
            elif response.status_code == 409:
                ConsoleLogger.write_log(
                    'warn',
                    __name__,
                    'create_block',
                    'Block was declined by the node {} because conflict '
                    'resolution is required. The process of conform '
                    'general state was runned.'.format(node.address)
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
                    'create_block',
                    'Block was declined because something went wrong on the'
                    ' peer node {}.'.format(node.address)
                )
        except requests.exceptions.ConnectionError:
            ConsoleLogger.write_log(
                'error',
                __name__,
                'create_block',
                'Block was declined because some problems with connection '
                'on the peer node {} were arised.'.format(node.address)
            )
            continue

    if corrupted_block_chain:
        response = {
            'message': 'Creating a block via broadcast failed. The local '
                       'block chain was replaced because it was corrupted. '
                       'Try again, please.'
        }
        return (jsonify(response), 200)
    elif verified_success:
        app.block_chain.add_block(block)
        app.open_txs.clear()
        Saver.save_data(app)

        response = {
            'message': 'A new block is added successfully.',
            'block': block.to_dict(),
            'funds': app.calculate_balance(Accountant())
        }
        return (jsonify(response), 201)
    else:
        response = {
            'message': 'Creating a local block and via broadcast failed.'
        }
        return (jsonify(response), 500)


def broadcast_block():
    app = Application.get_instance()

    if (app.wallet.public_key is None or
        app.wallet.private_key is None):
        response = {
            'message':
            'Reception a broadcastable block failed because the wallet is not set up.',
        }
        return (jsonify(response), 401)

    values = request.get_json()
    if not values:
        response = {'message': 'No data found.'}
        return (jsonify(response), 400)
    if 'block' not in values:
        response = {'message': 'Required data is missing.'}
        return (jsonify(response), 400)

    block = values['block']
    if block['index'] == app.block_chain.last_block.index + 1:
        tx_list_builder = TxListBuilder()
        tx_list = tx_list_builder.build(block['transactions'])

        proof_is_valid = Verifier.valid_proof(
            tx_list[:-1],
            block['previous_hash'],
            block['proof']
        )

        hashes_match = (block['previous_hash'] ==
                        Hasher.hash_block(app.block_chain.last_block))

        verified_success = False
        if proof_is_valid and hashes_match:
            verified_success = True
        
        if verified_success:
            app.block_chain.add_block(
                Block(
                    block['index'],
                    block['previous_hash'],
                    tx_list,
                    block['proof'],
                    block['timestamp']
                )
            )
            
            stored_transactions = app.open_txs.copy()

            for input_tx, tx in zip(
                block['transactions'],
                stored_transactions
            ):
                if (tx.sender == input_tx['sender'] and
                    tx.recipient == input_tx['recipient'] and
                    tx.amount == input_tx['amount'] and
                    tx.signature == input_tx['signature']):
                        app.open_txs.remove_tx(tx)

            Saver.save_data(app)
            response = {'message': 'A block is added successfully.'}
            return (jsonify(response), 201)
        else:
            response = {'message': 'A block seems invalid.'}
            return (jsonify(response), 409)
    elif block['index'] > app.block_chain.last_block.index:
        if app.conform_state(
            StateConformer(),
            BlockChainBuilder(),
            TxListBuilder()
        ):
            Saver.save_data(app)

        response = {
            'message': 'The block chain seems to differ from the local block '
                       'chain.'
        }

        return (jsonify(response), 200)
    else:
        response = {
            'message': 'The block chain seems to be shorter, a block not added.'
        }
        return (jsonify(response), 409)
