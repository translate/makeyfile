# -*- coding: utf-8 -*-

from mock import MagicMock, patch

from makeyfile.runners.command import CommandRunner


def test_runners_comand_call():
    runner = CommandRunner('x')

    def _cb(command, *args):
        assert command == "bar"
        assert args == (2, 3)
        return 23

    result = runner(_cb, "bar", 1, 2, 3)
    assert result == 23


def test_runners_comand_parse_module():
    runner = CommandRunner('x')
    assert runner.parse_module("foo.bar") == "foo.bar"
    assert runner.parse_module("foo7.bar23") == "foo7.bar23"


def test_runners_comand_parse_callable():
    runner = CommandRunner('x')
    assert runner.parse_callable("foo.bar") == "Command"
    assert runner.parse_callable("foo7.bar23") == "Command"


def test_runners_comand_resolve():
    runner = CommandRunner('x')

    with patch("makeyfile.runners.command.PythonRunner.resolve") as m:
        command_m = MagicMock(return_value=23)
        m.return_value = command_m
        result = runner.resolve("foo")
        assert result == 23
        assert m.call_args[0] == ("foo", )
        assert command_m.call_args[0] == ('x', )
