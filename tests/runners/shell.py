# -*- coding: utf-8 -*-

import os
import subprocess

from makeyfile.runners.shell import ShellRunner


def test_runners_py_resolve_runner():
    runner = ShellRunner('x')
    result = runner.resolve("some string")
    assert result == 'some string'
    result = runner.resolve(["1", "2", "3 and 4"])
    assert result == '123 and 4'


def test_runners_py_call():
    runner = ShellRunner('x')

    def _cb(command, *args, **kwargs):
        assert command == subprocess.call
        assert args == ('baz 2 3', )
        assert(
            sorted(kwargs.keys())
            == ['env', 'executable', 'shell'])
        assert kwargs['env'] == os.environ
        assert kwargs['executable'] == '/bin/bash'
        assert kwargs['shell'] is True
        return 23

    result = runner(_cb, "baz", "1", "2", "3")
    assert result == 23
