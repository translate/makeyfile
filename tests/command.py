# -*- coding: utf-8 -*-

import argparse
from contextlib import nested

from mock import MagicMock, PropertyMock, patch

import pytest

from makeyfile.command import Command
from makeyfile.exceptions import UnrecognizedMakeyError


def test_command_defaults():
    makey_m = MagicMock()
    command = Command(makey_m)
    assert command.makeyfile == makey_m


def test_command_resolver():
    makey_m = MagicMock()
    resolver_p = PropertyMock(return_value=23)
    type(makey_m).resolver = resolver_p
    resolver = Command(makey_m).resolver
    assert resolver == 23
    assert resolver_p.called


def test_command_commands():
    makey_m = MagicMock()
    commands_p = PropertyMock(return_value=23)
    resolver_p = PropertyMock()
    type(makey_m).resolver = resolver_p
    type(makey_m.resolver).commands = commands_p
    commands = Command(makey_m).commands
    assert commands == 23
    assert commands_p.called


def test_command_parser_class():
    makey_m = MagicMock()
    assert (
        Command(makey_m).parser_class
        == argparse.ArgumentParser)


def test_command_parser():
    makey_m = MagicMock()
    patches = [
        patch(
            'makeyfile.command.Command.parser_class',
            new_callable=PropertyMock),
        patch('makeyfile.command.Command.add_args')]

    with nested(*patches) as (parser_p, add_args_m):
        args_m = MagicMock(return_value=7)
        parser_p.return_value = args_m
        add_args_m.return_value = 23
        parser = Command(makey_m).parser
        assert parser == 23
        assert args_m.called
        assert add_args_m.call_args[0] == (7, )


def test_command_add_args():
    makey_m = MagicMock()
    parser_m = MagicMock()
    command = Command(makey_m)

    _patch = patch(
        'makeyfile.command.Command.commands',
        new_callable=PropertyMock)

    with _patch as p:
        p.return_value = dict(foo=23)
        result = command.add_args(parser_m)
        assert (
            parser_m.add_argument.call_args[0]
            == ('command',))
        assert (
            parser_m.add_argument.call_args[1]
            == {'action': 'store',
                'help': 'Command to run',
                'choices': ['foo']})
        assert p.called
        assert result is parser_m


def test_command_parse_args():
    makey_m = MagicMock()
    command = Command(makey_m)
    parser_m = MagicMock()
    command_m = MagicMock()
    result_p = PropertyMock(return_value=7)
    type(command_m).command = result_p

    _patches = [
        patch(
            'makeyfile.command.Command.parser',
            new_callable=PropertyMock)]

    with nested(*_patches) as (parser_p, ):
        parser_m.parse_known_args.return_value = [23]
        parser_p.return_value = parser_m
        result = command.parse_args("X")
        assert (
            parser_m.parse_known_args.call_args[0]
            == (("X", ), ))
        assert result == 23
        parser_m.parse_known_args.side_effect = SystemExit("die!")

        with pytest.raises(UnrecognizedMakeyError):
            result = command.parse_args("X")
