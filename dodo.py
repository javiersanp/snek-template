"""Script for task automation.

See: http://pydoit.org/
Note: Install doit with python3, preferably in a virtual environment
"""
import glob
import os
import webbrowser
from urllib.request import pathname2url

DOIT_CONFIG = {"default_tasks": ["check", "style", "test"], "verbosity": 2}
PYTEST_VERBOSITY = "-v"  # Set as "", "-v", "-vv" or "-vvv"
MIN_COVERAGE = "10"  # Test fails if coverage is under this value
LINE_LENGHT = "79"  # black don't have a config file

# Set file_dep to this to run task only when the code changes
PYTHON_FILES = [
    path for path in glob.iglob("**/*.py", recursive=True) if "{" not in path
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


def task__verchew():
    """Check system dependencies."""
    return {
        "file_dep": [".verchew.ini"],
        "actions": ["python bin/verchew --exit-code"],
    }


def task_install():
    """Install all dependencies in a virtual environment."""
    return {
        "file_dep": ["pyproject.toml"],
        "actions": ["poetry install"],
        "task_dep": ["_verchew"],
        "targets": ["poetry.lock"],
    }


def task_check():
    """Check diff of code formatters."""
    for action in [BLACK_CMD.format(diff="--diff"), "poetry run isort --diff"]:
        yield get_subtask(action, PYTHON_FILES)


def task_format():
    """Run code formatters."""
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


def task__showcov():
    # TODO: Read tox.ini [coverage:html] directory default
    cov_html = "file://" + pathname2url(
        os.path.abspath("docs/_build/coverage_html/index.html")
    )
    return {"actions": None, "teardown": [(webbrowser.open, (cov_html,))]}


def task__covhtml():
    return {"file_dep": [".coverage"], "actions": ["poetry run coverage html"]}


def task_coverage():
    """Generate a coverage html report."""
    return {
        "actions": None,
        "task_dep": ["test", "_covhtml"],
        "setup": ["_showcov"],
    }
