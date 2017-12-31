
from . import registry
from .discovery import Discovery
from .loader import Loader
from .resolver import Resolver


class Makeyfile(object):

    def __init__(self):
        self.registry = registry
        self.discovery = Discovery()
        self.loader = Loader()
        self.filepath = self.discovery.find()
        self.makey = self.loader.load(self.filepath)
        self.resolver = Resolver(self)
