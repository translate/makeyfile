makeyfile
=========

A very minimal runner that allows you to specify shell commands, python
code, or a sequence containing commands/code.

Inspired by the fact that people end up using ``Make`` to specify
build/test/run scripts for projects, despites its limited capabilities.

|build| |coverage|


Install
-------

.. code-block:: console

  $ pip install makeyfile


For development install

.. code-block:: console

  $ pip install -e git+git@github.com:phlax/makeyfile#egg=makeyfile
  $ pip install makeyfile[test]


Configuration
-------------

``makeyfile`` looks for a ``.Makeyfile.json`` in the current directory.

In this configuration file you can specify python callable code, shell
commands, or sequences that may contain any other python/shell/sequences.

Example configuration:

.. code-block:: json

    {
	"sequence": {
	    "command-sequence0": [
		"shell-command0",
		"shell-command1"
            ],
	    "command-sequence1": [
		"command-sequence0",
		"python-command1",
		"shell-command0"
            ],
	},
	"python": {
	    "python-command0": "some.module0.callable_code",
	    "python-command1": "some.module1.callable_code"
	},
	"shell": {
	    "shell-command0": "./runsomething",
	    "shell-command1": "run-something-else --with flags"
	}
    }

You can also specify shell and pythons paths. These are appended to
``$PYTHONPATH`` and ``$PATH`` before any scripts or code are run.

For example if you have some python code in a folder called ``scripts``
(``scripts/module0.py`` in the following example) and some executables
in a folder ``./some/custom/bin``, the following config will allow you to
call them.

.. code-block:: json

    {
	"scripts": ["./scripts"],
	"paths": ["./some/custom/.bin"],
	"python": {
	    "python-command0": "module0.callable_code"
	},
	"shell": {
	    "shell-command0": "run-something"
	}
    }


Usage
-----

Once configured you can call any of your sequences/code/commands using
the `makey` command.

.. code-block:: bash

    $ makey command-sequence0
    $ makey python-command0
    $ makey shell-command0


Passing args
------------

For python commands, all args specified when calling ``makey`` are passed
through to the python callable as ``argv``.

.. code-block:: bash

    $ makey python-command0 foo bar # python code receives ["foo", "bar"]


For shell commands, calling args (should be) appended to the specified command.

.. code-block:: bash

    $ makey shell-command0 foo bar # shell command is called with ``foo bar`` appended


For sequences, you cannot specify any additional command line args at runtime.



.. |build| image:: https://img.shields.io/travis/phlax/makeyfile/master.svg?style=flat-square
        :alt: Build Status
        :target: https://travis-ci.org/phlax/makeyfile/branches


.. |coverage| image:: https://img.shields.io/codecov/c/github/phlax/makeyfile/master.svg?style=flat-square
        :target: https://codecov.io/gh/phlax/makeyfile/branch/master
        :alt: Test Coverage
