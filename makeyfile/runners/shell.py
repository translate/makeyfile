
import os
import subprocess


from .base import BaseRunner


class ShellRunner(BaseRunner):

    def __call__(self, cb, command, *args):
        extra = ""
        if args[1:]:
            extra = " %s" % " ".join(args[1:])
        command = "%s%s" % (command, extra)
        return cb(
            subprocess.call,
            command,
            shell=True,
            executable="/bin/bash",
            env=os.environ)

    def resolve(self, command):
        return (
            "".join(command)
            if isinstance(command, list)
            else command)
