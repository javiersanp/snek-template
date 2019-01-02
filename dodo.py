"""Script for task automation.

See: http://pydoit.org/
Note: Install doit with python3, preferably in a virtual environment
"""
import glob
import os
import webbrowser
from urllib.request import pathname2url

DOIT_CONFIG = {
    "default_tasks": ["format", "style", "test"],
    "verbosity": 2,
    "template": "{name:<10} {doc}",
}
PYTEST_VERBOSITY = "-v"  # Set as "", "-v", "-vv" or "-vvv"
MIN_COVERAGE = "10"  # Test fails if coverage is under this value
LINE_LENGHT = "79"  # black don't have a config file

# Set file_dep to this to run task only when the code changes
PYTHON_FILES = [
    path for path in glob.iglob("**/*.py", recursive=True) if "{" not in path
]
# Set file_dep to this to run task only when the documentation changes
DOCS_FILES = [
    path for path in glob.iglob("**/*.md", recursive=True) if "{" not in path
]
BLACK_CMD = (
    "black -l "
    + LINE_LENGHT
    + r' {diff} --exclude "(\.venv|\.git|\{{|\.tox|build|dist)" .'
)


def get_subtask(cmd_action, file_dep=None):
    """Return a dictionary defining a substack for string 'cmd_action'."""
    if cmd_action.startswith("poetry run "):
        name = cmd_action.split(" ")[2]
    else:
        name = cmd_action.split(" ")[0]
    task = {"name": name, "actions": [cmd_action], "task_dep": ["install"]}
    if file_dep is not None:
        task["file_dep"] = file_dep
    return task


def open_in_browser(file_to_open):
    """Open a file in the web browser."""
    url = "file://" + pathname2url(os.path.abspath(file_to_open))
    webbrowser.open(url)


def show_task_doc(task):
    print("TODO: " + task.doc)


def show_more():

    def show_task(task):
        doc = task.__doc__ + "\n"
        meta = task()
        if "targets" in meta:
            doc += "    Targets: " + ", ".join(meta["targets"]) + "\n"
        if "file_dep" in meta:
            doc += "    File denpendencies: " + ", ".join(meta["file_dep"]) + "\n"
        task_dep = []
        if "task_dep" in meta:
            task_dep = [i for i in meta["task_dep"] if not i.startswith("_")]
        if len(task_dep) > 0:
            doc += "    Task denpendencies: " + ", ".join(task_dep) + "\n"
        print("doit " + task.__name__[5:] + doc)

    print("\n\ndoit")
    print("    Run the default tasks: " + str(DOIT_CONFIG["default_tasks"]))
    print("")
    for task in [task_install, task_init]:
        show_task(task)


# TODO
def task_init():
    """
    Initialize the git repository.

    Creates a empty git local, connect to your previously created remote
    repository, create the `develop` branch and checkout to it.
    """
    return {"actions": [show_task_doc], "targets": [".git"]}


def task__verchew():
    """Check system dependencies."""
    return {
        "file_dep": [".verchew.ini"],
        "actions": ["python bin/verchew --exit-code"],
    }


def task_install():
    """
    Install all dependencies in a virtual environment.
    
    The first step for your project. Check system dependencies, create a
    virtual environment if necessary and install the requirements.
    """
    return {
        "file_dep": ["pyproject.toml"],
        "actions": ["poetry install"],
        "task_dep": ["_verchew", "init"],
        "targets": ["poetry.lock"],
    }


def task_check():
    """Show the changes that the code formatters would apply."""
    for action in [BLACK_CMD.format(diff="--diff"), "poetry run isort --diff"]:
        yield get_subtask(action, PYTHON_FILES)


def task_format():
    """Run code formatters and apply it's changes."""
    for action in [BLACK_CMD.format(diff=""), "poetry run isort -y"]:
        yield get_subtask(action, PYTHON_FILES)


def task_style():
    """Check code styling."""
    for action in [
        "poetry run flake8",
        "poetry run pydocstyle",
        "poetry run isort --check-only -rc .",
    ]:
        yield get_subtask(action, PYTHON_FILES)


def task_test():
    """Run tests."""
    pytest_cmd = "poetry run pytest {v} --cov --cov-fail-under={mc}".format(
        v=PYTEST_VERBOSITY, mc=MIN_COVERAGE
    )
    return {"actions": [pytest_cmd], "file_dep": PYTHON_FILES}


# TODO
def task_test_all():
    """Run tests using different Python versions."""
    return {"basename": "test-all", "actions": [show_task_doc]}


def task__covhtml():
    return {
        "file_dep": [".coverage"],
        "actions": ["poetry run coverage html"],
        "targets": ["htmlcov", "htmlcov/index.html"],
    }


def task_coverage():
    """Generate and show the coverage html report."""
    return {
        "actions": [(open_in_browser, ("htmlcov/index.html",))],
        "task_dep": ["test", "_covhtml"],
    }


def task__docshtml():
    return {
        "file_dep": DOCS_FILES,
        "actions": ["poetry run mkdocs build"],
        "targets": ["site", "site/index.html"],
    }


def task_docs():
    """Generate the HTML documentation."""
    return {
        "actions": [(open_in_browser, ("site/index.html",))],
        "task_dep": ["_docshtml"],
    }


def task_docs_serve():
    """Show the documentation and coverage watching for changes."""
    # https://github.com/gorakhargosh/watchdog (sphinx)
    return {
        "basename": "docs-serve",
        "actions": ["poetry run mkdocs serve"],
    }


# TODO
def task_release():
    """Bump the current version and release to the repository master branch."""
    return {"actions": [show_task_doc]}


# TODO
def task_build():
    """Build source and wheel package."""
    return {"actions": [show_task_doc]}


# TODO
def task_publish():
    """Publish to PyPI."""
    return {"actions": [show_task_doc]}


# TODO
def task_clean_all():
    """Remove all build, test, coverage and Python artifacts."""
    # calls to doit clean task ?
    return {"basename": "clean-all", "actions": [show_task_doc]}


# TODO
def task_more():
    """Show extended help on this script and its workflow."""
    return {"actions": [show_more]}
