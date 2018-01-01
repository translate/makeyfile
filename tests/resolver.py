# -*- coding: utf-8 -*-

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


def test_resolver_resolve_registered():
    makey_mock = MagicMock()
    runner_mock = MagicMock()
    runner_mock.resolve = MagicMock(return_value=23)

    makey_p = PropertyMock(return_value=dict(foo=dict(bar="baz")))
    type(makey_mock).makey = makey_p

    runners_p = PropertyMock(return_value=dict(foo=runner_mock))
    type(makey_mock).runners = runners_p

    resolver = Resolver(makey_mock)

    with pytest.raises(UnrecognizedMakeyError):
        resolver.resolve_registered('NOT', 'EXISTS')
    assert not runners_p.called

    with pytest.raises(UnrecognizedMakeyError):
        resolver.resolve_registered('foo', 'ALSO NOT EXISTS')
    assert not runners_p.called

    result = resolver.resolve_registered("foo", "bar")
    assert runners_p.called
    assert runner_mock.resolve.called
    assert runner_mock.resolve.call_args[0][0] == "baz"
    assert result == ('foo', 23)


def test_resolver_resolve_command():
    makey_mock = MagicMock()
    runner_mock = MagicMock()
    runner_mock.resolve = MagicMock(return_value=23)

    makey_p = PropertyMock(return_value=dict(foo=dict(bar="baz")))
    type(makey_mock).makey = makey_p

    runners_p = PropertyMock(return_value=dict(foo=runner_mock))
    type(makey_mock).runners = runners_p

    resolver = Resolver(makey_mock)
    with patch('makeyfile.resolver.Resolver.resolve_registered') as m:
        m.side_effect = UnrecognizedMakeyError
        with pytest.raises(UnrecognizedMakeyError):
            resolver.resolve('DOES NOT EXIST')
        assert m.call_args[0] == ('foo', 'DOES NOT EXIST')
    assert makey_p.called

    with patch('makeyfile.resolver.Resolver.resolve_registered') as m:
        resolver.resolve('foo')
        assert m.call_args[0] == ('foo', 'foo')
