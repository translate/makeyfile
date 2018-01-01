
from collections import OrderedDict

from .command import CommandRunner
from .py import PythonRunner
from .sequence import SequenceRunner
from .shell import ShellRunner


def register_defaults(registry):
    registry.register("runner", "sequence", SequenceRunner)
    registry.register("runner", "python", PythonRunner)
    registry.register("runner", "shell", ShellRunner)
    registry.register("runner", "command", CommandRunner)


class Runners(object):

    def __init__(self, makeyfile):
        self._runners = OrderedDict()
        self.makeyfile = makeyfile
        self.load_runners()

    def load_runners(self):
        for name, runner in self.makeyfile.registry["runner"].items():
            self[name] = runner(self.makeyfile)

    def __getitem__(self, k):
        return self._runners[k]

    def __setitem__(self, k, v):
        self._runners[k] = v

    def __contains__(self, k):
        return k in self._runners

    def __iter__(self):
        return iter(self._runners.keys())

    def keys(self):
        return self._runners.keys()

    def items(self):
        return self._runners.items()

    def values(self):
        return self._runners.values()
