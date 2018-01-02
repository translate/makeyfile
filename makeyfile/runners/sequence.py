
import functools

from .base import BaseRunner


class SequenceRunner(BaseRunner):

    def __call__(self, cb, commands, *args):
        return cb(
            functools.partial(
                self._runcommands,
                commands))

    def _run(self, command):
        _command = []
        if self.makeyfile.options["verbosity"]:
            _command.append(
                "-v%s"
                % self.makeyfile.options["verbosity"])
        _command.append(command)
        return self.makeyfile.runner.run(*_command)

    def _runcommands(self, commands):
        result = [
            (command.split(" ")[0]
             if self._run(command)
             else None)
            for command
            in commands]
        if any(result):
            return "Failed: %s" % filter(lambda x: x, result)
