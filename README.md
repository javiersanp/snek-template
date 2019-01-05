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
* Optional automatic code formatting with [Black](https://github.com/ambv/black) and isort.

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

Usage
-----

Create a `git` empty repository (whitout any accesory files like README, .gitignore).

Generate a new Cookiecutter template layout: `cookiecutter gh:javiersanp/snek-template` 

You will be prompted to enter these values:

* **project_name**: The display name for your project. This is used in documentation, so spaces and any characters are fine here.
* **project_slug**: The namespace of your Python package. This should be Python import-friendly. Typically, it is the slugified version of project_name.
* **project_short_description**: A 1-sentence description of what your Python package does.
* **full_name**: Your full name.
* **email**: Your email address.
* **git_user_name**: Your git account.
* **repo_name**: The name of your project repository.
* **repository**: The url of the project git repository.
* **version**: The starting version number of the package.
* **license**: Legal stuff about reusing your project. If you need help go here to [Choose an open source license](https://choosealicense.com).
* **docs_generator**: Choose the tool MkDocs or Sphinx to generate the static site of the documentation.

Change to the newly created project folder. For example, if your *'project_slug'* is demo: `cd demo`.

Then you can install with:

    doit install

The install task will execute three steeps:

1. Check the system for the [required](#Requirements) tools.
2. Initialize the repository. Create a empty local git, connect to your previously created remote repository, create the `develop` branch and checkout to it.
3. Create a virtual environment if there is not one active. Install in it the project requirements.

You can use poetry to add aditional requirements. For example:

    poetry add pendulum
    poetry add --dev mock

To list all the availlable DoIt [tasks](tasks.md) run:

    doit list

Read more about [poetry](https://poetry.eustace.io/docs/) or [DoIt](http://pydoit.org/contents.html) in their documentation.

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

