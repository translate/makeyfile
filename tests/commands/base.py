# -*- coding: utf-8 -*-

from contextlib import nested

from mock import patch

import pytest

from makeyfile.commands.base import BaseCommand


def test_cmd_base_defaults():
    command = BaseCommand("x")
    assert command.makeyfile == "x"


def test_cmd_base_call():
    command = BaseCommand("x")
    patches = [
        patch('makeyfile.commands.base.BaseCommand.parse_args'),
        patch('makeyfile.commands.base.BaseCommand.run')]

    with nested(*patches) as (parse_m, run_m):
        parse_m.return_value = dict(foo=7)
        run_m.return_value = 23
        result = command(1, 2, 3)
        assert parse_m.call_args[0] == (1, 2, 3)
        assert run_m.call_args[1] == dict(foo=7)
        assert result == 23


def test_cmd_base_run():
    command = BaseCommand("x")

    with pytest.raises(NotImplementedError):
        command.run(foo=7, bar=23)


def test_cmd_base_parse_args():
    command = BaseCommand("x")
    assert command.parse_args(1, 2, 3) == {}
