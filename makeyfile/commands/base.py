

class BaseCommand(object):

    def __init__(self, makeyfile):
        self.makeyfile = makeyfile

    def __call__(self, *args):
        return self.run(**self.parse_args(*args))

    def parse_args(self, *args):
        return {}

    def run(self, **kwargs):
        raise NotImplementedError
