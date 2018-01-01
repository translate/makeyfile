
from .py import PythonRunner


class CommandRunner(PythonRunner):

    def parse_module(self, command):
        return command

    def parse_callable(self, command):
        return "Command"

    def resolve(self, command):
        command = super(CommandRunner, self).resolve(command)
        return command(self.makeyfile)
