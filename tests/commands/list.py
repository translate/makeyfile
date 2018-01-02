# -*- coding: utf-8 -*-

from mock import MagicMock, patch

from makeyfile.commands.list import Command


def test_cmd_list():
    makey_m = MagicMock()
    makey_m.resolver.commands.items.return_value = (
        ("foo0", "bar0"),
        ("foo1", "bar1"),
        ("foo2", "bar2"))
    command = Command(makey_m)

    with patch('makeyfile.commands.list.sys') as sys_m:
        result = command(1, 2, 3)
        assert result is None
        assert makey_m.resolver.commands.items.called
        assert (
            sys_m.stdout.write.call_args_list[0][0]
            == ('foo0 (bar0)\nfoo1 (bar1)\nfoo2 (bar2)', ))
        assert (
            sys_m.stdout.write.call_args_list[1][0]
            == ("\n", ))
