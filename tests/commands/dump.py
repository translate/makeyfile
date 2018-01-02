# -*- coding: utf-8 -*-

from contextlib import nested

from mock import MagicMock, patch

from makeyfile.commands.dump import Command


def test_cmd_dump():
    makey_m = MagicMock()
    makey_m.load_makeyfile.return_value = 7
    command = Command(makey_m)
    patches = [
        patch('makeyfile.commands.dump.json'),
        patch('makeyfile.commands.dump.sys')]

    with nested(*patches) as (json_m, sys_m):
        json_m.dumps.return_value = 23
        result = command(1, 2, 3)
        assert result is None
        assert json_m.dumps.call_args[0] == (7, )
        assert (
            json_m.dumps.call_args[1]
            == dict(indent=4, separators=(',', ': ')))
        assert (
            sys_m.stdout.write.call_args_list[0][0]
            == (23, ))
        assert (
            sys_m.stdout.write.call_args_list[1][0]
            == ("\n", ))
