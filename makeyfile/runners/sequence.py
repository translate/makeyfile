
import functools


class SequenceRunner(object):

    def __call__(self, cb, makeyfile, commands, *args):
        return cb(
            functools.partial(
                self._runcommands,
                makeyfile,
                args[0],
                commands))

    def _runcommands(self, makeyfile, sequence, commands):
        return any(
            (command.split(" ")[0]
             if makeyfile.runner.run(command)
             else None)
            for command
            in commands)

    def resolve(self, command):
        return command
