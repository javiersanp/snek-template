Automation tool
===============

This is a list of all the availlable task defined in `dodo.py`. They can be executed using the `doit [task]*` command.

Installation
------------

Install all project dependencies in a virtual environment::

    doit install

Development
-----------

Usually you will run the doit command without arguments::

    doit

This will execute the default tasks in this order: check, style, test.

To manually check the changes that the code formatters would apply::

    doit check

Run code formatters and apply it's changes::

    doit format

Check code styling::

    doit style

Run tests::

    doit test

Run tests with tox using different Python versions::

    doit test-all

Generate and show the coverage html report::

    doit coverage

Generate the HTML documentation::

    doit docs

Show the documentation and coverage watching for changes::

    doit docs-serve

Release
-------

Bump the current version and release to the repository master branch::

    doit release --part minor

Build source and wheel package::

    doit build

Publish to PyPI::

    doit publish

Remove all build, test, coverage and Python artifacts::

    doit clean-all

Some options
------------

A task will run only if their target files don't exists, or it dependent files have been modified. You can force the execution with the `always` option::

    doit --always check

Note that you can run multiple tasks in a single invocation::

    doit check style

You can also run a particular target::

    doit style:flake8

For more info about DoIt check it [documentation](http://pydoit.org/contents.html) and the command line help::

    doit help
