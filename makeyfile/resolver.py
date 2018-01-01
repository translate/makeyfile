
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
            _commands += zip(self.makey[k].keys(), [k] * len(self.makey[k]))
        return OrderedDict(_commands)

    def resolve(self, command):
        if command not in self.commands:
            raise UnrecognizedMakeyError()
        resolved = self.commands[command]
        return resolved, self.makey[resolved][command]
