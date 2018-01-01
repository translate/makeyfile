# -*- coding: utf-8 -*-

from contextlib import nested

from mock import MagicMock, PropertyMock, patch

import pytest

from makeyfile.exceptions import MakeyError
from makeyfile.runners.py import PythonRunner


def test_runners_py_resolve_module():
    runner = PythonRunner('x')

    with patch("makeyfile.runners.py.import_module") as m:
        m.return_value = 23
        result = runner.resolve_module('foo.bar.BazRun')
        assert result == 23
        assert m.call_args[0] == ('foo.bar', )

    with patch("makeyfile.runners.py.import_module") as m:
        m.side_effect = ImportError('no such module')

        with pytest.raises(MakeyError) as e:
            runner.resolve_module('foo.bar.BazRun')
        assert m.call_args[0] == ('foo.bar', )
        assert e.value[1] == m.side_effect


def test_runners_py_resolve_callable():
    runner = PythonRunner('x')
    module_m = MagicMock()
    run_p = PropertyMock(return_value=23)
    type(module_m).BazRun = run_p
    result = runner.resolve_callable(module_m, "foo.bar.BazRun")
    assert result == 23
    assert run_p.called is True


def test_runners_py_resolve_callable_bad():
    runner = PythonRunner('x')
    error = AttributeError('oops')

    # magic mock doesnt handle AttributeError side effects
    class MockedModule():

        @property
        def BazRun(self):
            raise error

    with pytest.raises(MakeyError) as e:
        runner.resolve_callable(MockedModule(), "foo.bar.BazRun")
    assert (
        e.value[0]
        == 'Misconfigured makey file, callable ("BazRun") not found')
    assert e.value[1] is error


def test_runners_py_resolve_runner():
    runner = PythonRunner('x')

    patches = [
        patch("makeyfile.runners.py.PythonRunner.resolve_module"),
        patch("makeyfile.runners.py.PythonRunner.resolve_callable")]

    with nested(*patches) as (module_m, callable_m):
        module_m.return_value = 23
        callable_m.return_value = 17
        result = runner.resolve("foo.bar.BazRun")
        assert module_m.call_args[0] == ('foo.bar.BazRun', )
        assert callable_m.call_args[0] == (23, 'foo.bar.BazRun')
        assert result == 17


def test_runners_py_call():
    runner = PythonRunner('x')

    def _cb(command, *args):
        assert command == "baz"
        assert args == (2, 3)
        return 23

    result = runner(_cb, "bar", "baz", 1, 2, 3)
    assert result == 23
