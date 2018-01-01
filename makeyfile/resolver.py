
from collections import OrderedDict

from .exceptions import UnrecognizedMakeyError


class Resolver(object):

    def __init__(self, makeyfile):
        self.makeyfile = makeyfile
        self.makey = makeyfile.makey

    @property
    def commands(self):
        _commands = []
        for k in self.makeyfile.runners.keys():
            if k in self.makey.keys():
                _commands += zip(
                    self.makey[k].keys(),
                    [k] * len(self.makey[k]))
        return OrderedDict(_commands)

    def get_handler(self, name):
        return self.makeyfile.runners[name]

    def resolve(self, command):
        if command not in self.commands:
            raise UnrecognizedMakeyError()
        resolved = self.commands[command]
        return (
            resolved,
            self.get_handler(resolved).resolve(self.makey[resolved][command]))
