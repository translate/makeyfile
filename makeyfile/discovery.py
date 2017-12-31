
import os

from .exceptions import MakeyDiscoveryError


class Discovery(object):

    makeyfile_name = '.Makeyfile.json'

    def _recurse_parent(self, path):
        path = os.path.abspath(path)
        if self.makeyfile_name in os.listdir(path):
            return os.path.join(path, self.makeyfile_name)
        if os.path.dirname(path) == path:
            raise MakeyDiscoveryError(
                "Loading makeyfile (%s) failed"
                % self.makeyfile_name)
        return self._recurse_parent(os.path.dirname(path))

    def find(self):
        return self._recurse_parent(".")
