

import sys
from os.path import dirname

from .command import Command
from .contextmanagers import isolated, runner
from .exceptions import MakeyError
from .makeyfile import Makeyfile


class Runner(object):

    def __init__(self, makeyfile):
        self.makeyfile = makeyfile
        self.makeyfile.runner = self
        self.makey = makeyfile.makey

    @property
    def command(self):
        return Command(self.makeyfile)

    @property
    def root(self):
        return dirname(self.makeyfile.filepath)

    def handle(self, *args):
        _isolated = isolated(
            self.root,
            self.makey.get("scripts", []),
            self.makey.get("paths", []),
            self.makey.get("env", {}))
        with _isolated:
            return self.run(*args)

    def get_handler(self, handler):
        return self.makeyfile.runners[handler]

    def run(self, *args, **kwargs):
        handler, resolved = self.command.resolve(args[0])
        with runner(handler.capitalize(), args[0], resolved) as cb:
            return self.get_handler(handler)(
                cb, resolved, *args)


def main():
    try:
        sys.exit(Runner(Makeyfile()).handle(*sys.argv[1:]))
    except MakeyError as e:
        sys.stdout.write(
            "\n".join(reversed([str(x) for x in e] + ["\nMakey Error!\n"])))
        sys.exit(e)


if __name__ == '__main__':
    main()
