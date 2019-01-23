Snek Template
=============

[![](https://travis-ci.org/javiersanp/snek-template.png)](https://travis-ci.org/javiersanp/snek-template) [![](https://circleci.com/gh/javiersanp/snek-template.png?style=shield)](https://travis-ci.org/javiersanp/snek-template)

Another [cookiecutter](https://github.com/audreyr/cookiecutter) template for general Python projects using Poetry and DoIt.

Features
--------

* System dependencies version checker with [verchew](https://github.com/jacebrowning/verchew).
* Dependency management and packaging with [Poetry](https://poetry.eustace.io/).
* Automated tasks workflow with [DoIt](http://pydoit.org/). Run tasks only when the dependent files change.
* Testing with [pytest](https://pytests.org).
* Metrics of test [coverage](https://coverage.readthedocs.io) and [mccabe](https://github.com/The-Compiler/pytest-mccabe) complexity.
* Style enforcement with [flake8](http://flake8.pycqa.org), [isort](https://github.com/timothycrosley/isort) and [pydocsstyle](http://www.pydocstyle.org/).
* Optional automatic code formatting with [Black](https://github.com/ambv/black) and isort.
* Generation of documentation with [Sphinx](http://www.sphinx-doc.org) or [mkdocs](https://www.mkdocs.org/).
* Edit documentation on the fly with [livereload](https://github.com/lepture/python-livereload) server for Sphinx and built-in Mkdocs feature.
* Build matrix with [tox](https://tox.readthedocs.io).
* [Bump version](https://github.com/c4urself/bump2version) and release to master branch with one command.
* Continous Integration with [Travis](https://travis-ci.org/) or [CircleCI](https://circleci.com).

Planned Features
----------------

* Continous Integration with [Jenkins](https://jenkins.io).

**Optionally**

* Auto-release to [PyPI](https://pypi.org/).

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
* **docs_generator**: Choose the tool MkDocs or Sphinx to generate the documentation site.
* **command_line_interface**: Optionally add a Command-line Interface with [Click](https://github.com/pallets/click).
* **continous_integration**: Choose your CI platform.

Change to the newly created project folder. For example, if your *'project_slug'* is demo: `cd demo`.

Then you can install with::

    doit install

The install task will execute this steeps:

1. Check the system for the [required](#Requirements) tools.
2. Create a virtual environment if there is not one active. Install in it the project requirements.

Initialize the repository with::

    doit init-repo

This create a empty local git, connect it to your previously created remote repository, tag the initial version, push all files to the `master` branch, create the `develop` branch and checkout to it. It will be the first version release. It's recommended to follow this [Git branching model](https://nvie.com/posts/a-successful-git-branching-model/). Check out the [gitflow](https://github.com/nvie/gitflow/) extension to git.

You can use poetry to add aditional requirements. For example::

    poetry add pendulum
    poetry add --dev mock

To list all the availlable DoIt [tasks](tasks.md) run::

    doit list

Read more about [poetry](https://poetry.eustace.io/docs/) or [DoIt](http://pydoit.org/contents.html) in their documentation.

Extra context
-------------

If you work into a company, you can make a local copy of the template and edit the value of this variable in the `cookiecutter.json` file. It will be used in the software copyright statements.

* **_company**: Full name of your company if any, else leave it blank.

Project structure
-----------------

These are the files and directories created by the template:

* **_AUTHORS.md_**: Add your credits here.
* **_bin_**: Directory for utility scripts.
* **_.bumpversion.cfg_**: Bumpversion configuration file.
* **_CHANGELOG.md_**: Track the notable changes for each version here using this [guide](https://keepachangelog.com/en/0.3.0/). Always have an "Unreleased" section at the top for keeping track of any changes. Bumpversion will add automatically the new version and release date. If you don't want to use it just delete this file.
* **_CONTRIBUTING.md_**: Information for new developers.
* **_{project_slug}_**: Python package for your project.
* **_docs_**: Directory for the documentation source files. It will be generated in the *site* directory, both for MkDocs and Sphinx. Code coverage reports will be generated in *site/htmlcov*.
* **_dodo.py_**: Tasks definition script for DoIt.
* **_doit.cfg_**: Doit configuration file. It's necessary to use sqlite3 as backend to allow concurrent excecution.
* **_.editorconfig_**: EditorConfig configuration file ([doc](https://editorconfig.org/)).
* **_.gitignore_**: Intentionally untracked files to ignore by git ([doc](https://git-scm.com/docs/gitignore)).
* **_LICENSE_**: Legal stuff about reusing your project.
* **_mkdocs.yml_**: Configuration file for MkDocs.
* **_pyproject.toml_**: Project metadata and dependencies specification.
* **_README.md_**: Describe your project here.
* **_tests_**: Directory for code testing.
* **_tox.ini_**: Configuration file for tox, but also many other tools.
* **_.verchew.ini_**: System dependencies definition for _bin/verchew_.

Similar projects
----------------

* https://github.com/audreyr/cookiecutter-pypackage
* https://github.com/claws/cookiecutter-python-project
* https://github.com/jacebrowning/template-python
* https://github.com/elgertam/cookiecutter-pipenv
* https://github.com/sdss/python_template

Credits
-------

* The snek name comes from the [Amir Rachum tutorial](https://amir.rachum.com/blog/2017/07/28/python-entry-points/) used for the tempate code.

