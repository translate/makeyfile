# -*- coding: utf-8 -*-

import json

import os
import pytest

from makeyfile import registry
from makeyfile.discovery import Discovery
from makeyfile.exceptions import MakeyDiscoveryError
from makeyfile.loader import Loader
from makeyfile.makeyfile import Makeyfile
from makeyfile.resolver import Resolver


def test_makeyfile_defaults(tmpdir):
    os.chdir(str(tmpdir))

    with pytest.raises(MakeyDiscoveryError):
        makey = Makeyfile()

    makeypath = str(tmpdir.join(Discovery.makeyfile_name))

    with open(makeypath, "wb") as f:
        f.write(json.dumps(dict(foo=23)))

    makey = Makeyfile()
    assert makey.registry is registry
    assert isinstance(makey.loader, Loader)
    assert isinstance(makey.resolver, Resolver)
    assert makey.resolver.makeyfile is makey
    assert makey.resolver.makey is makey.makey
    assert isinstance(makey.discovery, Discovery)
    assert makey.filepath == makey.discovery.find()
    assert makey.makey == dict(foo=23)
