#!/usr/bin/env python3
from sys import argv, exit
from packages import main as package_manager


def print_hello():
    print("Hello")


def fatal_error(msg):
    exit(f'ERROR: {msg}')


if len(argv) == 1:
    print_hello()
else:
    command = argv[1]
    if command == 'install':
        if len(argv) != 3:
            fatal_error('Install require only one argument')
        program = argv[2]
        package_manager.install(program)

