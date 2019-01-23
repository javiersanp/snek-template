Automation tool
===============

This project uses `DoIt <http://pydoit.org>`_ for task automation. These are its advantages:

* Time saving since the tasks will not be executed if the files they depend on have not been modified.
* Summarize complex operations in individual commands.
* It facilitates learning the workflow to new collaborators.
* Enforces tasks to run in the correct order. Ensure that the code is tested and style linted before merge or push.

This is a list of all the availlable tasks defined in ``dodo.py``. They can be executed using the ``doit [task]*`` command.

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

Note for pyenv users: don't forget to explicitly enable the Python versions
used by tox, for example::

    pyenv local 3.7.1 3.6.7 2.7.15

Generate and show the coverage html report::

    doit coverage

Generate and show the HTML documentation::

    doit docs

Show the documentation and coverage watching for changes::

    doit docs-serve

Release
-------

Merge the current branch with the positional argument (default master) and push
it. The test-all task will run before this to ensure you don't merge untested
code::

    doit merge [branch-to-merge-into]

Bump the part of the current version given in the positional argument and 
release to the repository master branch. Availlable choices are:

* major: when you make incompatible API changes.
* minor: when you add functionality in a backwards-compatible manner.
* patch: when you make backwards-compatible bug fixes.

The test-all task will run before this to ensure you don't publish untested code::

    doit release [part_of_version_to_increase]

Build source and wheel package::

    doit build

Publish to PyPI::

    doit publish

Some options
------------

A task will run only if their target files don't exists, or it dependent files have been modified. You can force the execution with the ``always`` option::

    doit --always check

Note that you can run multiple tasks in a single invocation::

    doit check style

You can also run a particular target::

    doit style:flake8

For more info about DoIt check it `documentation <http://pydoit.org/contents.html>`_ and the command line help::

    doit help
