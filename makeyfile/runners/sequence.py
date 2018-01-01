
import functools

from .base import BaseRunner


class SequenceRunner(BaseRunner):

    def __call__(self, cb, commands, *args):
        return cb(
            functools.partial(
                self._runcommands,
                args[0],
                commands))

    def _run(self, command):
        return self.makeyfile.runner.run(command)

    def _runcommands(self, sequence, commands):
        return any(
            (command.split(" ")[0]
             if self._run(command)
             else None)
            for command
            in commands)

    def resolve(self, command):
        return command
