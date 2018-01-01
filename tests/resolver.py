# -*- coding: utf-8 -*-

from collections import OrderedDict
from contextlib import nested

import pytest

from mock import MagicMock, PropertyMock, patch

from makeyfile.exceptions import UnrecognizedMakeyError
from makeyfile.resolver import Resolver


def test_resolver_defaults():
    with pytest.raises(TypeError):
        Resolver()

    makey_mock = MagicMock()
    _p = PropertyMock(return_value=[23])
    type(makey_mock).makey = _p
    resolver = Resolver(makey_mock)

    assert _p.called
    assert resolver.makey == [23]


def test_resolver_commands():
    makey_mock = MagicMock()
    makey_p = PropertyMock(
        return_value=OrderedDict(
            (("foo0", OrderedDict((("bar0a", "baz0a"), ("bar0b", "baz0b")))),
             ("foo1", OrderedDict((("bar1a", "baz1a"), ("bar1b", "baz1b")))))))
    type(makey_mock).makey = makey_p
    runners_p = PropertyMock(
        return_value=dict(foo0="x", foo1="y"))
    type(makey_mock).runners = runners_p
    resolver = Resolver(makey_mock)
    commands = resolver.commands
    assert runners_p.called
    assert (
        commands.items()
        == [('bar0a', 'foo0'),
            ('bar0b', 'foo0'),
            ('bar1a', 'foo1'),
            ('bar1b', 'foo1')])


def test_resolver_get_handler():
    makey_mock = MagicMock()
    runners_p = PropertyMock(return_value=dict(foo=23))
    type(makey_mock).runners = runners_p
    resolver = Resolver(makey_mock)
    result = resolver.get_handler("foo")
    assert result == 23
    assert runners_p.called


def test_resolver_resolve_command():
    makey_mock = MagicMock()
    runner_mock = MagicMock()
    runner_mock.resolve = MagicMock(return_value=23)

    makey_p = PropertyMock(return_value=dict(foo=dict(bar="baz")))
    type(makey_mock).makey = makey_p

    runners_p = PropertyMock(return_value=dict(foo=runner_mock))
    type(makey_mock).runners = runners_p

    resolver = Resolver(makey_mock)
    _patches = [
        patch(
            'makeyfile.resolver.Resolver.commands',
            new_callable=PropertyMock),
        patch(
            'makeyfile.resolver.Resolver.get_handler')]

    with nested(*_patches) as (commands_m, handler_m):
        commands_m.return_value = dict(bar="foo")
        with pytest.raises(UnrecognizedMakeyError):
            resolver.resolve('DOES NOT EXIST')
        assert commands_m.called

    with nested(*_patches) as (commands_m, handler_m):
        commands_m.return_value = dict(bar="foo")
        resolve_m = MagicMock()
        resolve_m.resolve.return_value = 23
        handler_m.return_value = resolve_m
        result = resolver.resolve('bar')
        assert handler_m.call_args[0] == ('foo', )
        assert (
            resolve_m.resolve.call_args[0]
            == ('baz',))
        assert result == ('foo', 23)
