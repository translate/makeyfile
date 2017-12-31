
from .exceptions import UnrecognizedMakeyError


class Resolver(object):

    def __init__(self, makeyfile):
        self.makeyfile = makeyfile
        self.makey = makeyfile.makey

    def resolve(self, command):
        for k in self.makeyfile.registry["runner"].keys():
            try:
                return self.resolve_registered(k, command)
            except UnrecognizedMakeyError:
                pass
        raise UnrecognizedMakeyError()

    def resolve_registered(self, registered, command):
        try:
            command = self.makey[registered][command]
            return (
                registered,
                self.makeyfile.registry["runner"][registered].resolve(command))
        except KeyError:
            raise UnrecognizedMakeyError(
                'Unrecognized makey command: %s'
                % command)
