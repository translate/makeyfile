
import json
import sys

from .base import BaseCommand


class Command(BaseCommand):

    def run(self, **kwargs):
        sys.stdout.write(
            json.dumps(
                self.makeyfile.load_makeyfile(),
                indent=4, separators=(',', ': ')))
        sys.stdout.write("\n")
