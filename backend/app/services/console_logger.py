#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime


__all__ = [
    'ConsoleLogger',
]

TYPES_INFO = {'info': 'INFO', 'warn': 'WARNING', 'error': 'ERROR'}


class ConsoleLogger:
    """ A helper class for write log to console about application work. """

    @classmethod
    def __new__(cls):
        raise TypeError('ConsoleLogger is a static class.')

    @staticmethod
    def write_log(*args):
        """ Writes a log to console. """
        print(
            '[{date_time}] - {module_name} - {function_name} - {type_message}'
            ' - {message}'
            .format(
                type_message=TYPES_INFO[args[0]],
                module_name=args[1],
                function_name=args[2],
                message=args[3],
                date_time=datetime.now()
            )
        )
