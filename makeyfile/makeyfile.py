
import os

from . import registry
from .discovery import Discovery
from .loader import Loader
from .resolver import Resolver
from .runners import Runners


class Makeyfile(object):
    command_filename = "makeyfile.commands.json"

    def __init__(self):
        self.registry = registry
        self.runners = Runners(self)
        self.discovery = Discovery()
        self.loader = Loader()
        self.makey = self.load()
        self.resolver = Resolver(self)
        self.options = dict(verbosity=None)

    @property
    def filepath(self):
        return self.discovery.find()

    @property
    def command_filepath(self):
        return os.path.join(
            os.path.dirname(__file__),
            self.command_filename)

    def load_commands(self):
        return self.loader.load(self.command_filepath)

    def load_makeyfile(self):
        return self.loader.load(self.filepath)

    def load(self):
        makey = self.load_commands()
        makey.update(self.load_makeyfile())
        return makey
