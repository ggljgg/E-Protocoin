#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app.routes import api_routes
from argparse import ArgumentParser
from app.services.loader import Loader
from app.services.app_builder import AppBuilder


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)

    args = parser.parse_args()
    port = args.port
    
    app_builder = AppBuilder(__name__, port)
    app = app_builder.build(*Loader.load_data(port))

    app.register_routes(api_routes, url_prefix='/api/v1')
    app.run()
