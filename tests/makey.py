# -*- coding: utf-8 -*-

import json
import os
from contextlib import nested

import pytest

from mock import MagicMock, patch

from makeyfile import makeyfile
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
    assert makey.command_filename == "makeyfile.commands.json"


def test_makeyfile_command_filepath(tmpdir):
    os.chdir(str(tmpdir))

    makeypath = str(tmpdir.join(Discovery.makeyfile_name))

    with open(makeypath, "wb") as f:
        f.write(json.dumps(dict(foo=23)))

    makey = Makeyfile()
    assert (
        makey.command_filepath
        == os.path.join(
            os.path.dirname(makeyfile.__file__),
            makey.command_filename))


def test_makeyfile_load_commands(tmpdir):
    os.chdir(str(tmpdir))
    makeypath = str(tmpdir.join(Discovery.makeyfile_name))

    with open(makeypath, "wb") as f:
        f.write(json.dumps(dict(foo=23)))

    with patch("makeyfile.makeyfile.Loader") as m:
        loader_m = MagicMock()
        loader_m.load.return_value = 23
        m.return_value = loader_m
        makey = Makeyfile()
        result = makey.load_commands()
        assert result == 23
        assert loader_m.load.call_args[0] == (makey.command_filepath, )


def test_makeyfile_load_makeyfile(tmpdir):
    os.chdir(str(tmpdir))
    makeypath = str(tmpdir.join(Discovery.makeyfile_name))

    with open(makeypath, "wb") as f:
        f.write(json.dumps(dict(foo=23)))

    with patch("makeyfile.makeyfile.Loader") as m:
        loader_m = MagicMock()
        loader_m.load.return_value = 23
        m.return_value = loader_m
        makey = Makeyfile()
        result = makey.load_makeyfile()
        assert result == 23
        assert loader_m.load.call_args[0] == (makey.filepath, )


def test_makeyfile_load(tmpdir):
    os.chdir(str(tmpdir))
    makeypath = str(tmpdir.join(Discovery.makeyfile_name))

    with open(makeypath, "wb") as f:
        f.write(json.dumps(dict(foo=23)))

    patches = [
        patch("makeyfile.makeyfile.Makeyfile.load_commands"),
        patch("makeyfile.makeyfile.Makeyfile.load_makeyfile")]

    with nested(*patches) as (commands_m, makey_m):
        commands_m.return_value = dict(foo=7)
        makey_m.return_value = dict(bar=23)
        makey = Makeyfile()
        result = makey.load()
        assert result == {'foo': 7, 'bar': 23}
        assert commands_m.called
        assert makey_m.called
