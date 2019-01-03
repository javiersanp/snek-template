Installation
------------

Install all project dependencies in a virtual environment.

    doit install

This task will be executed before the install to initialize the git repository. It creates a empty local git, connect to your previously created remote repository, create the `develop` branch and checkout to it.

    doit init

Development
-----------

Usually you will run the doit command without arguments. This will execute the default tasks in this order: check, style, test, docs.

    doit

To manually check the changes that the code formatters would apply:

    doit check

Run code formatters and apply it's changes:

    doit format

Check code styling.

    doit style

Run tests.

    doit test

Run tests using different Python versions.

    doit test-all

Generate and show the coverage html report.

    doit coverage

Generate the HTML documentation.

    doit docs

Show the documentation and coverage watching for changes.

    doit docs-serve

Release
-------

Bump the current version and release to the repository master branch.

    doit release

Build source and wheel package.

    doit build

Publish to PyPI.

    doit publish

Remove all build, test, coverage and Python artifacts.

    doit clean-all

