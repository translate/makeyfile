

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

    def resolve(self, *args):
        makey_args = []
        for arg in args:
            if arg.startswith("-"):
                makey_args.append(arg)
                continue
            makey_args.append(arg)
            break
        parsed = self.command.parse_args(*makey_args)
        self.makeyfile.options["verbosity"] = int(parsed.verbosity)
        return (
            (makey_args, )
            + self.makeyfile.resolver.resolve(parsed.command))

    def run(self, *args, **kwargs):
        makey_args, handler, resolved = self.resolve(*args)
        _runner = runner(
            handler.capitalize(),
            makey_args[-1],
            resolved,
            verbosity=self.makeyfile.options['verbosity'])
        with _runner as cb:
            return self.get_handler(handler)(
                cb, resolved, *args[len(makey_args) - 1:])


def main():
    try:
        sys.exit(Runner(Makeyfile()).handle(*sys.argv[1:]))
    except MakeyError as e:
        sys.stdout.write(
            "\n".join(reversed([str(x) for x in e] + ["\nMakey Error!\n"])))
        sys.exit(e)


if __name__ == '__main__':
    main()
