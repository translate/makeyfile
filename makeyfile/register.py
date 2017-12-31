
from collections import OrderedDict

from .runners import register_defaults


class MakeyfileRegistry(object):

    def __init__(self):
        self._registry = OrderedDict()
        self.register_defaults()

    def register(self, name, k, v):
        self._registry[name] = self._registry.get(name, OrderedDict())
        self._registry[name][k] = v

    def __contains__(self, k):
        return k in self._registry

    def __iter__(self):
        return iter(self._registry.keys())

    def __getitem__(self, name):
        return self._registry[name]

    def register_defaults(self):
        register_defaults(self)
