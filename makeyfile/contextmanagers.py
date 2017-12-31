
import os
import sys
from collections import OrderedDict
from contextlib import contextmanager


@contextmanager
def isolated(root, scripts, paths, environ):
    original_directory = os.getcwd()
    os.chdir(root)
    original_path = os.environ["PATH"]
    orig_sys_path = os.environ["PATH"].split(":")
    orig_python_path = sys.path[:]
    sys.path = OrderedDict.fromkeys(
        orig_python_path + scripts).keys()
    os.environ["PATH"] = ":".join(
        OrderedDict.fromkeys(
            orig_sys_path
            + [os.path.abspath(
                os.path.expanduser(p))
               for p
               in paths]).keys())
    yield
    sys.path = orig_python_path
    os.environ["PATH"] = original_path
    os.chdir(original_directory)


@contextmanager
def runner(handler, name, command):
    sys.stdout.write(
        ">>> %s '%s' started: %s \n"
        % (handler, name, command))

    def _run(*args, **kwargs):
        try:
            result = args[0](*args[1:], **kwargs)
        except KeyboardInterrupt:
            result = 0
        sys.stdout.write(
            "<<< %s '%s' %s %s \n"
            % (handler,
               name,
               result and "failed" or "complete",
               result if isinstance(result, str) else ""))
        return result
    yield _run
