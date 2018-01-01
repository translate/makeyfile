
import json
from collections import OrderedDict

from .exceptions import MakeyError


class Loader(object):

    def load(self, filepath):
        try:
            with open(filepath, 'r') as makeyfile:
                try:
                    return json.loads(
                        makeyfile.read(),
                        object_pairs_hook=OrderedDict)
                except ValueError as e:
                    raise MakeyError('Failed to parse the makeyfile', e)
        except IOError as e:
            raise MakeyError('Makeyfile appears to be missing', e)
