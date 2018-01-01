
from importlib import import_module

from makeyfile.exceptions import MakeyError

from .base import BaseRunner


class PythonRunner(BaseRunner):

    def parse_callable(self, command):
        return command.split('.')[-1]

    def parse_module(self, command):
        return '.'.join(command.split('.')[:-1])

    def resolve_module(self, command):
        try:
            return import_module(self.parse_module(command))
        except ImportError as e:
            raise MakeyError(
                ('Misconfigured makey file, callable ("%s") not found'
                 % self.parse_module(command)),
                e)

    def resolve_callable(self, module, command):
        try:
            return getattr(module, self.parse_callable(command))
        except AttributeError as e:
            raise MakeyError(
                ('Misconfigured makey file, callable ("%s") not found'
                 % self.parse_callable(command)),
                e)

    def resolve(self, command):
        return self.resolve_callable(
            self.resolve_module(command),
            command)
