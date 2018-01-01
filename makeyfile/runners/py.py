
from importlib import import_module

from makeyfile.exceptions import MakeyError

from .base import BaseRunner


class PythonRunner(BaseRunner):

    def __call__(self, cb, makeyfile, command, *args):
        return cb(command, *args[1:])

    def resolve_module(self, command):
        try:
            return import_module('.'.join(command.split('.')[:-1]))
        except ImportError as e:
            raise MakeyError(
                ('Misconfigured makey file, callable ("%s") not found'
                 % '.'.join(command.split('.')[:-1])),
                e)

    def resolve_callable(self, module, command):
        try:
            return getattr(module, command.split('.')[-1])
        except AttributeError as e:
            raise MakeyError(
                ('Misconfigured makey file, callable ("%s") not found'
                 % command.split('.')[-1]),
                e)

    def resolve(self, command):
        return self.resolve_callable(
            self.resolve_module(command),
            command)
