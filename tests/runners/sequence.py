# -*- coding: utf-8 -*-

import functools

from mock import MagicMock, patch

from makeyfile.runners.sequence import SequenceRunner


def test_runners_sequence_resolve_runner():
    runner = SequenceRunner('x')
    assert runner.resolve('foo') == 'foo'
    assert runner.resolve('bar') == 'bar'


def test_runners_sequence_call():
    runner = SequenceRunner('x')

    def _cb(*args):
        assert len(args) == 1
        partial = args[0]
        assert partial.func == runner._runcommands
        assert partial.args == ([1, 2, 3], )
        assert isinstance(partial, functools.partial)
        return 23

    result = runner(_cb, [1, 2, 3], "foo", "bar")
    assert result == 23


def test_runners_sequence_runcommands():
    runner = SequenceRunner('x')

    with patch("makeyfile.runners.sequence.SequenceRunner._run") as m:
        m.return_value = 23
        result = runner._runcommands(
            ["foo bar baz",
             "foo0 bar baz",
             "foo1 bar baz"])
        assert (
            [x[0] for x in m.call_args_list]
            == [('foo bar baz', ),
                ('foo0 bar baz', ),
                ('foo1 bar baz', )])
        assert result == ['foo', 'foo0', 'foo1']

    with patch("makeyfile.runners.sequence.SequenceRunner._run") as m:
        m.return_value = None
        result = runner._runcommands(
            ["foo bar baz",
             "foo0 bar baz",
             "foo1 bar baz"])
        assert (
            [x[0] for x in m.call_args_list]
            == [('foo bar baz', ),
                ('foo0 bar baz', ),
                ('foo1 bar baz', )])
        assert result is None

    with patch("makeyfile.runners.sequence.SequenceRunner._run") as m:

        def _mock_run(*args):
            if "foo0" in args[0]:
                return True
            return False

        m.side_effect = _mock_run
        result = runner._runcommands(
            ["foo bar baz",
             "foo0 bar baz",
             "foo1 bar baz"])
        assert (
            [x[0] for x in m.call_args_list]
            == [('foo bar baz', ),
                ('foo0 bar baz', ),
                ('foo1 bar baz', )])
        assert result == ['foo0']


def test_runners_sequence_run():
    makey_m = MagicMock()
    runner = SequenceRunner(makey_m)
    makey_m.runner.run.return_value = 23
    assert runner._run('foo') == 23
    assert makey_m.runner.run.call_args[0] == ('foo',)
    assert runner._run('bar') == 23
    assert makey_m.runner.run.call_args[0] == ('bar',)
