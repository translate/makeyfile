
import os
import subprocess


class ShellRunner(object):

    def __call__(self, cb, makeyfile, command, *args):
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
