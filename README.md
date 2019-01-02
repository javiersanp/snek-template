Snek Template
=============

Another cookicutter template for general Python projects.

This project aims to build a [cookiecutter](https://github.com/audreyr/cookiecutter) template for personal use.

Planned Features
----------------

* Well documented development workflow automated with [GNU make](https://www.gnu.org/software/make/).
* Dependency management and packaging with [Poetry](https://poetry.eustace.io/).
* Testing with [pytest](https://pytests.org).
* Style enforcement with [flake8](http://flake8.pycqa.org).
* Set the template for my particular set of code style and analysis tools:
    * TODO: define.
* Generation of documentation with [Sphinx](http://www.sphinx-doc.org) \[or [mkdocs](https://www.mkdocs.org/) or none\].
* Build matrix with [tox](https://tox.readthedocs.io).
* Continous Integration with [Travis](https://travis-ci.org/) \[, [CircleCI](https://circleci.com) or [Jenkins](https://jenkins.io)\].
* Choose between many [open source licenses](https://choosealicense.com/).
* Option to copyright (for example a Company name). It will be the author by default.

**Optionally**

* Addapt the template to be used both for libraries and applications.
* Option to choose between mkdocs, Sphinx or no docs.
* Add configuration for many CI: Travis, Jenkins and maybe CircleCI.
* Auto-release to [PyPI](https://pypi.org/) (optional).

Requirements
------------

Install `cookiecutter` command line: `pip install cookiecutter` 

Usage
-----

Generate a new Cookiecutter template layout: `cookiecutter gh:javirsanp/snek-template` 

You will be prompted to enter these values:

project_name
    The display name for your project. This is used in documentation, so spaces and any characters are fine here.
project_slug
    The namespace of your Python package. This should be Python import-friendly. Typically, it is the slugified version of project_name.
project_short_description
    A 1-sentence description of what your Python package does.
full_name
    Your full name.
email
    Your email address.
version
    The starting version number of the package.
license
    Legal stuff about reusing your project. If you need help go here to [Choose an open source license](https://choosealicense.com).


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

