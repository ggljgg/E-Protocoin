#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import jsonify, request
from ..services.saver import Saver
from app.application import Application
from ..services.accountant import Accountant


__all__ = [
    'get_wallet',
    'create_wallet',
]


def get_wallet():
    app = Application.get_instance()

    if (app.wallet.public_key is not None and
        app.wallet.private_key is not None):

        response = {
            'message': 'The wallet uploaded successfully.',
            'funds': app.calculate_balance(Accountant()),
            'wallet keys': app.wallet.to_dict()
        }
        return (jsonify(response), 200)
    else:
        response = {'message': 'Create the wallet first.'}
        return (jsonify(response), 200)


def create_wallet():
    app = Application.get_instance()

    app.wallet.assign_keys(
        *app.wallet.generate_keys()
    )

    if (app.wallet.public_key is not None and
        app.wallet.private_key is not None):
    
        if Saver.save_data(app):
            response = {
                'message': 'The wallet created successfully.',
                'funds': app.calculate_balance(Accountant()),
                'wallet keys': app.wallet.to_dict()
            }
            return (jsonify(response), 201)
        else:
            response = {'message': 'Saving the wallet failed.'}
            return (jsonify(response), 500)
