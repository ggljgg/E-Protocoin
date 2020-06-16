#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ..models.node import Node
from ..services.saver import Saver
from flask import jsonify, request
from ..application import Application


__all__ = [
    'get_nodes',
    'create_node',
    'delete_node',
]


def get_nodes():
    app = Application.get_instance()

    if (app.wallet.public_key is None or
        app.wallet.private_key is None):
        response = {
            'message':
            'Getting the nodes failed because the wallet is not set up.'
        }
        return (jsonify(response), 401)

    response = {
        'message': 'The nodes collection is fetched successfully',
        'all nodes': app.network.to_list()
    }
    return (jsonify(response), 200)


def create_node():
    app = Application.get_instance()

    if (app.wallet.public_key is None or
        app.wallet.private_key is None):
        response = {
            'message':
            'Adding a new node failed because the wallet is not set up.'
        }
        return (jsonify(response), 401)

    values = request.get_json()

    if not values:
        response = {'message': 'No data found.'}
        return (jsonify(response), 400)
    if 'address' not in values:
        response = {'message': 'No node data found.'}
        return (jsonify(response), 400)

    address = values['address']
    app.network.add_node(Node(address))
    Saver.save_data(app)

    response = {
        'message': 'A new node is added successfully.',
        'all nodes': app.network.to_list()
    }
    return (jsonify(response), 201)


def delete_node(address):
    app = Application.get_instance()

    if (app.wallet.public_key is None or
        app.wallet.private_key is None):
        response = {
            'message':
            'Removing the node failed because the wallet is not set up.'
        }
        return (jsonify(response), 401)

    if (address is None) or (address == ''):
        response = {'message': 'No node data found.'}
        return (jsonify(response), 400)

    app.network.remove_node(address)
    Saver.save_data(app)

    response = {
        'message': 'The node is removed successfully.',
        'all nodes': app.network.to_list()
    }
    return (jsonify(response), 200)
