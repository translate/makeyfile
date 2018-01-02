
import sys


from .base import BaseCommand


class Command(BaseCommand):

    def run(self, **args):
        sys.stdout.write(
            "\n".join(
                ("%s (%s)" % (command, runner))
                for command, runner
                in self.makeyfile.resolver.commands.items()))
        sys.stdout.write("\n")
