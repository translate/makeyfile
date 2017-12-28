# -*- coding: utf-8 -*-

import os
import sys

from makeyfile.contextmanagers import isolated, runner


def test_cm_isolated(tmpdir):
    syspath = sys.path
    orig_directory = os.getcwd()
    orig_path = os.environ["PATH"]

    with isolated(str(tmpdir), [], [], {}):
        assert os.getcwd() == str(tmpdir)
        # this removes duplicates, so not necessarily ==
        assert set(sys.path) == set(syspath)
        assert os.environ["PATH"] == orig_path

    assert sys.path == syspath
    assert os.environ["PATH"] == orig_path
    assert os.getcwd() == orig_directory


def test_cm_isolated_python(tmpdir):
    syspath = sys.path
    orig_directory = os.getcwd()
    orig_path = os.environ["PATH"]

    with isolated(str(tmpdir), ["foo", "bar"], [], {}):
        assert os.getcwd() == str(tmpdir)
        assert sys.path[-2:] == ["foo", "bar"]
        assert os.environ["PATH"] == orig_path

    assert sys.path == syspath
    assert os.environ["PATH"] == orig_path
    assert os.getcwd() == orig_directory


def test_cm_isolated_paths(tmpdir):
    syspath = sys.path
    orig_directory = os.getcwd()
    orig_path = os.environ["PATH"]

    with isolated(str(tmpdir), [], ["foo", "bar"], {}):
        assert os.getcwd() == str(tmpdir)
        # this removes duplicates, so not necessarily ==
        assert set(sys.path) == set(syspath)
        assert (
            [str(tmpdir.join(x)) for x in ["foo", "bar"]]
            == os.environ["PATH"].split(":")[-2:])
    assert sys.path == syspath
    assert os.environ["PATH"] == orig_path
    assert os.getcwd() == orig_directory


def test_cm_runner(capsys):

    with runner("foo", "bar", "baz") as cb:

        def _run(*args, **kwargs):
            out, err = capsys.readouterr()
            assert out == u">>> foo 'bar' started: baz \n"
            assert not err
            assert args == (1, 2)
            assert kwargs == dict(other=3)
            return 0

        result = cb(_run, 1, 2, other=3)
        assert result == 0
        out, err = capsys.readouterr()
        assert out == u"<<< foo 'bar' complete  \n"
        assert not err


def test_cm_runner_fail(capsys):

    with runner("foo", "bar", "baz") as cb:

        def _run(*args, **kwargs):
            out, err = capsys.readouterr()
            assert out == u">>> foo 'bar' started: baz \n"
            assert not err
            assert args == (1, 2)
            assert kwargs == dict(other=3)
            return 4

        result = cb(_run, 1, 2, other=3)
        assert result == 4
        out, err = capsys.readouterr()
        assert out == u"<<< foo 'bar' failed  \n"
        # err?
        assert not err


def test_cm_runner_fail_result(capsys):

    with runner("foo", "bar", "baz") as cb:

        def _run(*args, **kwargs):
            out, err = capsys.readouterr()
            assert out == u">>> foo 'bar' started: baz \n"
            assert not err
            assert args == (1, 2)
            assert kwargs == dict(other=3)
            return "oops"

        result = cb(_run, 1, 2, other=3)
        assert result == "oops"
        out, err = capsys.readouterr()
        assert out == u"<<< foo 'bar' failed oops \n"
        # err?
        assert not err


def test_cm_runner_interrupt(capsys):

    with runner("foo", "bar", "baz") as cb:

        def _run(*args, **kwargs):
            out, err = capsys.readouterr()
            assert out == u">>> foo 'bar' started: baz \n"
            assert not err
            raise KeyboardInterrupt
        result = cb(_run, 1, 2, other=3)
        assert result == 0
        out, err = capsys.readouterr()
        assert out == u"<<< foo 'bar' complete  \n"
        assert not err
