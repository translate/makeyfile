# -*- coding: utf-8 -*-

from collections import OrderedDict

import pytest

from mock import MagicMock, PropertyMock

from makeyfile.runners import Runners


def test_runners_runners():
    with pytest.raises(TypeError):
        Runners()

    makey_m = MagicMock()
    foo_m = MagicMock(return_value=7)
    bar_m = MagicMock(return_value=23)
    baz_m = MagicMock(return_value=43)
    registry_p = PropertyMock(
        return_value=dict(
            runner=OrderedDict(
                (('foo', foo_m),
                 ('bar', bar_m),
                 ('baz', baz_m)))))
    type(makey_m).registry = registry_p

    runners = Runners(makey_m)
    assert foo_m.call_args[0] == (makey_m, )
    assert bar_m.call_args[0] == (makey_m, )
    assert baz_m.call_args[0] == (makey_m, )

    assert 'foo' in runners
    assert 'bar' in runners
    assert 'baz' in runners
    assert list(runners) == ['foo', 'bar', 'baz']
    assert runners.keys() == ['foo', 'bar', 'baz']
    assert runners.values() == [7, 23, 43]
    assert (
        runners.items()
        == [('foo', 7), ('bar', 23), ('baz', 43)])
    assert runners['foo'] == 7
