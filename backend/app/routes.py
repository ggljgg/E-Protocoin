#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Blueprint
from .views.wallet_view import *
from .views.network_view import *
from .views.tx_list_view import * 
from .views.block_chain_view import *


__all__ = [
    'api_routes',
]

api_routes = Blueprint('api', __name__)

api_routes.add_url_rule(
    '/wallet',
    'get_wallet',
    get_wallet
)

api_routes.add_url_rule(
    '/wallet',
    'post_wallet',
    create_wallet,
    methods=['POST']
)

api_routes.add_url_rule(
    '/block',
    'get_blocks',
    get_blocks
)

api_routes.add_url_rule(
    '/block',
    'post_block',
    create_block,
    methods=['POST']
)

api_routes.add_url_rule(
    '/transaction',
    'get_transactions',
    get_transactions
)

api_routes.add_url_rule(
    '/transaction',
    'post_transaction',
    create_transaction,
    methods=['POST']
)

api_routes.add_url_rule(
    '/node',
    'get_nodes',
    get_nodes
)

api_routes.add_url_rule(
    '/node',
    'post_node',
    create_node,
    methods=['POST']
)

api_routes.add_url_rule(
    '/node/<address>',
    'delete_node',
    delete_node,
    methods=['DELETE']
)

api_routes.add_url_rule(
    '/broadcast-transaction',
    'broadcast_transaction',
    broadcast_transaction,
    methods=['POST']
)

api_routes.add_url_rule(
    '/broadcast-block',
    'broadcast_block',
    broadcast_block,
    methods=['POST']
)
