#!/usr/bin/env python3
# pyright: strict
import sys
import os

from argparse import ArgumentParser
from typing import Type
from pathlib import Path

# Calculate the directory above this file to add to the Python path
current_script_path = Path(os.path.abspath(__file__))
project_root_directory = current_script_path.parent.parent
sys.path.append(str(project_root_directory))

if True:  # prevent formatter from re-ordering these imports
    from lconfig.commands.list_config_command import ListConfigCommand
    from lconfig.commands.command import Command

"""
This is the entry point for the linux configuration manager program. It parses 
the command line arguments, initializes the commands and runs the command.

run `cli.py --help` for instructions
"""


def main():

    parser = ArgumentParser(
        prog='Linux Config Manager CLI',
        description='Tool suit to create, manage and apply system configurations from config files.',
    )
    subparsers = parser.add_subparsers(
        help='available commands',
        dest='command',
    )

    commands: dict[str, Type[Command]] = {
        ListConfigCommand.get_name(): ListConfigCommand,
    }

    for commandCls in commands.values():
        commandCls.add_subparser(subparsers)

    parsed_args = parser.parse_args()
    commands_name = parsed_args.command

    if commands_name is None:
        parser.print_help()
        return

    command: Command = commands[commands_name].create_from_arguments(
        parsed_args)
    command.run()


if __name__ == '__main__':
    main()
