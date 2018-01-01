

class BaseRunner(object):

    def __init__(self, makeyfile):
        self.makeyfile = makeyfile

    def __call__(self, cb, command, *args):
        return cb(command, *args[1:])

    def resolve(self, command):
        return command
