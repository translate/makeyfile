# -*- coding: utf-8 -*-

from collections import OrderedDict

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


def test_resolver_resolve_command():
    makey_mock = MagicMock()
    runner_mock = MagicMock()
    runner_mock.resolve = MagicMock(return_value=23)

    makey_p = PropertyMock(return_value=dict(foo=dict(bar="baz")))
    type(makey_mock).makey = makey_p

    runners_p = PropertyMock(return_value=dict(foo=runner_mock))
    type(makey_mock).runners = runners_p

    resolver = Resolver(makey_mock)
    _patch = patch(
        'makeyfile.resolver.Resolver.commands',
        new_callable=PropertyMock)

    with _patch as m:
        m.return_value = dict(bar="foo")
        with pytest.raises(UnrecognizedMakeyError):
            resolver.resolve('DOES NOT EXIST')
        assert m.called

    with _patch as m:
        m.return_value = dict(bar="foo")
        result = resolver.resolve('bar')
        assert result == ('foo', 'baz')
