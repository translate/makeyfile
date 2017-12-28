# -*- coding: utf-8 -*-

import json

import pytest

from makeyfile.exceptions import MakeyError
from makeyfile.loader import Loader


def test_loader_defaults():
    # can instantiate with no args
    assert isinstance(Loader(), Loader)


def test_loader_load(tmpdir):
    loader = Loader()

    with pytest.raises(MakeyError):
        loader.load("/path/does/not/exist")

    foopath = str(tmpdir.join("foo.json"))

    with open(foopath, "wb") as f:
        f.write("'not valid json'")

    with pytest.raises(MakeyError):
        loader.load(foopath)

    barpath = str(tmpdir.join("bar.json"))

    with open(barpath, "wb") as f:
        f.write(json.dumps(dict(baz=23)))

    result = loader.load(barpath)
    assert result["baz"] is 23
