# -*- coding: utf-8 -*-

import sys
from contextlib import contextmanager, nested

import pytest

from mock import MagicMock, PropertyMock, patch

from makeyfile.exceptions import MakeyError
from makeyfile.runner import Runner, main
from makeyfile.makeyfile import Makeyfile


def test_runner_bad_no_makeyfile(tmpdir):
    with tmpdir.as_cwd():
        with pytest.raises(MakeyError) as e:
            Makeyfile()
        assert (
            e.value[0]
            == 'Loading makeyfile (.Makeyfile.json) failed')


def test_runner_defaults():
    with pytest.raises(TypeError):
        Runner()

    makey_mock = MagicMock()
    _p = PropertyMock(return_value=[23])
    type(makey_mock).makey = _p
    _r = PropertyMock()
    type(makey_mock).runner = _r

    runner = Runner(makey_mock)
    assert _r.call_args[0][0] is runner
    assert _p.called
    assert runner.makey == [23]


def test_runner_command():
    makey_m = MagicMock()
    makey_makey_p = PropertyMock(return_value=[23])
    type(makey_m).makey = makey_makey_p
    runner = Runner(makey_m)

    with patch('makeyfile.runner.Command') as command_m:
        command_m.return_value = 23
        command = runner.command
        assert command == 23


def test_runner_run():
    handler = MagicMock(return_value=7)
    makey_mock = MagicMock()
    _p = PropertyMock(return_value=[23])
    type(makey_mock).makey = _p
    _r = PropertyMock()
    type(makey_mock).runner = _r

    runner = Runner(makey_mock)

    patches = [
        patch('makeyfile.runner.Runner.command', new_callable=PropertyMock),
        patch('makeyfile.runner.Runner.get_handler'),
        patch('makeyfile.runner.runner')]

    with nested(*patches) as (command_p, handler_m, runner_m):
        resolve_m = MagicMock()
        resolve_m.resolve.return_value = ("somehandler", 2)
        command_p.return_value = resolve_m
        cm = MagicMock()
        cm.__enter__.return_value = 23
        runner_m.return_value = cm
        handler_m.return_value = handler
        result = runner.run("foo", "bar", "baz", foo=True)
        assert resolve_m.resolve.call_args[0] == ("foo", )
    assert handler_m.call_args[0] == ("somehandler", )
    assert handler.call_args[0] == (23, 2, 'foo', 'bar', 'baz')
    assert result == 7


def test_runner_get_handler():
    makey_mock = MagicMock()
    makey_p = PropertyMock(return_value=[23])
    type(makey_mock).makey = makey_p
    runner_p = PropertyMock()
    type(makey_mock).runner = runner_p
    runners_p = PropertyMock(return_value=dict(x=23))
    type(makey_mock).runners = runners_p
    runner = Runner(makey_mock)
    result = runner.get_handler("x")
    assert result == 23
    assert runners_p.called


def test_runner_root():
    makey_mock = MagicMock()
    makey_p = PropertyMock(return_value=dict(scripts=7, paths=13, env=23))
    type(makey_mock).makey = makey_p
    runner_p = PropertyMock()
    type(makey_mock).runner = runner_p
    filepath_p = PropertyMock(return_value=113)
    type(makey_mock).filepath = filepath_p
    runner = Runner(makey_mock)
    with patch('makeyfile.runner.dirname') as m:
        m.return_value = 117
        root = runner.root
        assert filepath_p.called
        assert m.call_args[0] == (113,)
        assert root == 117


def test_runner_handle():
    makey_mock = MagicMock()
    makey_p = PropertyMock(return_value=dict(scripts=7, paths=13, env=23))
    type(makey_mock).makey = makey_p
    runner_p = PropertyMock()
    type(makey_mock).runner = runner_p
    handler_p = PropertyMock()
    handler_p.__getitem__ = MagicMock(return_value=23)
    registry_p = PropertyMock(return_value=dict(runner=handler_p))
    type(makey_mock).registry = registry_p
    runner = Runner(makey_mock)
    _patches = [
        patch('makeyfile.runner.isolated'),
        patch('makeyfile.runner.Runner.run'),
        patch('makeyfile.runner.Runner.root', new_callable=PropertyMock)]
    with nested(*_patches) as (m_isolated, m_run, m_root):
        m_isolated.__enter__.return_value.name = ''
        m_run.return_value = 43
        m_root.return_value = 17
        result = runner.handle("foo", "bar", "baz")
        assert (
            m_isolated.call_args[0]
            == (17, 7, 13, 23))
        assert result == 43


def test_runner_main():
    _patches = [
        patch('makeyfile.runner.Runner'),
        patch('makeyfile.runner.Makeyfile')]

    @contextmanager
    def mangle_sys_argv(argv=()):
        old_argv = sys.argv
        sys.argv = list(argv)
        yield
        sys.argv = old_argv

    def _run(argv=(), return_value=0, side_effect=None):
        with mangle_sys_argv(argv):
            with nested(*_patches) as (runner_m, makey_m):
                with pytest.raises(SystemExit) as e:
                    if side_effect:
                        makey_m.side_effect = side_effect
                    makey_m.return_value = 23
                    handler_m = MagicMock()
                    handle_m = MagicMock(return_value=return_value)
                    handler_m.handle = handle_m
                    runner_m.return_value = handler_m
                    main()
        return e, makey_m, runner_m, handle_m
    e, makey_m, runner_m, handle_m = _run()
    assert makey_m.called is True
    assert not makey_m.call_args[0]
    assert runner_m.call_args[0] == (23, )
    assert handle_m.call_args[0] == ()
    assert e.value.code == 0

    e, makey_m, runner_m, handle_m = _run(["foo", "bar", "baz"])
    assert makey_m.called is True
    assert not makey_m.call_args[0]
    assert runner_m.call_args[0] == (23, )
    assert handle_m.call_args[0] == ("bar", "baz")
    assert e.value.code == 0

    _error = MakeyError('oops')
    e, makey_m, runner_m, handle_m = _run(
        ["foo", "bar", "baz"],
        side_effect=_error)
    assert e.value.code is _error
