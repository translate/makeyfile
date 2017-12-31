
from .py import PythonRunner
from .sequence import SequenceRunner
from .shell import ShellRunner


def register_defaults(registry):
    registry.register("runner", "sequence", SequenceRunner())
    registry.register("runner", "python", PythonRunner())
    registry.register("runner", "shell", ShellRunner())
