Snek Template
=============

Another cookicutter template for general Python projects.

This project aims to build a [cookiecutter](https://github.com/audreyr/cookiecutter) template for personal use.

Features
--------

* Dependency management and packaging with [Poetry](https://poetry.eustace.io/).
* Automated tasks workflow with [DoIt](http://pydoit.org/).
* Testing with [pytest](https://pytests.org).
* Style enforcement with [flake8](http://flake8.pycqa.org), [isort](https://github.com/timothycrosley/isort) and [pydocsstyle](http://www.pydocstyle.org/).
* Optional automatic code formatting with [Black](https://github.com/ambv/black)
* Choose between many [open source licenses](https://choosealicense.com/).

Planned Features
----------------

* Generation of documentation with [Sphinx](http://www.sphinx-doc.org) \[or [mkdocs](https://www.mkdocs.org/) or none\].
* Build matrix with [tox](https://tox.readthedocs.io).
* Continous Integration with [Travis](https://travis-ci.org/) \[, [CircleCI](https://circleci.com) or [Jenkins](https://jenkins.io)\].

**Optionally**

* Addapt the template to be used both for libraries and applications.
* Option to choose between mkdocs, Sphinx or no docs.
* Add configuration for many CI: Travis, Jenkins and maybe CircleCI.
* Auto-release to [PyPI](https://pypi.org/) (optional).

Requirements
------------

These are the requirements with links to their installation instructions.

* [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html).
* [Poetry](https://poetry.eustace.io/docs/)
* [DoIt](http://pydoit.org/install.html).

I suggest you to first install poetry following their recommended way:

    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

Then install [Pipsi](https://github.com/mitsuhiko/pipsi):

    curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python

And use it to install cookiecutter and doit:

    pipsi install cookiecutter doit


Usage
-----

Create a `git` empty repository (whitout any accesory files like README, .gitignore).

Generate a new Cookiecutter template layout: `cookiecutter gh:javirsanp/snek-template` 

You will be prompted to enter these values:

* **project_name**: The display name for your project. This is used in documentation, so spaces and any characters are fine here.
* **project_slug**: The namespace of your Python package. This should be Python import-friendly. Typically, it is the slugified version of project_name.
* **project_short_description**: A 1-sentence description of what your Python package does.
* **full_name**: Your full name.
* **email**: Your email address.
* **git_user_name**: Your git account.
* **git_repository**: The url of the project git repository.
* **version**: The starting version number of the package.
* **license**: Legal stuff about reusing your project. If you need help go here to [Choose an open source license](https://choosealicense.com).

Change to the newly created project folder. For example, if your *'project_slug'* is demo: `cd demo`.

Get familiar with the deveopment workflow with:

    doit more-help

Then you can install with

    doit install


Workflow
--------

The first step is to check system dependencies, create a virtual environment and install the project requirements.

    doit install

When you run the `install` task, first `init` will be executed. This task creates a empty git local repository, connects to your previously created remote repository, creates the `develop` branch and checkout to it.

    doit init

    doit install

To run the code tests, just:

    doit

This will run the default tasks: `style` and `test`.

To run the code tests:

    doit test

To validate code styling:

    doit style

If you want to show the changes that the code formatters would apply:

    doit check

And if you want to apply this changes to your code:

    doit format

You can use poetry to add aditional requirements. For example:

    poetry add pendulum
    poetry add --dev mock




Extra context
-------------

If you work into a company, you can make a local copy of the template and edit the `{{cookiecutter.project_slug}}/extra_context.j2` file.

* **company**: Full name of your company if any, else leave it blank.
* **company_short**: Acronym of your company if any, else leave it blank.

Goals
-----

Apply testing, documentation and good practices.
Achive a nice developing workflow.
Learn to use CI tools.

Similar projects
----------------

* https://github.com/audreyr/cookiecutter-pypackage
* https://github.com/claws/cookiecutter-python-project
* https://github.com/jacebrowning/template-python
* https://github.com/elgertam/cookiecutter-pipenv

Credits
-------

* The snek name comes from the [Amir Rachum tutorial](https://amir.rachum.com/blog/2017/07/28/python-entry-points/) used for the tempate code.

