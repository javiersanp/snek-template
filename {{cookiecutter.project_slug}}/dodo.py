"""Script for task automation.

See: http://pydoit.org/
Note: Install doit with python3, preferably in a virtual environment
"""
import glob
import os
import webbrowser
from urllib.request import pathname2url

DOIT_CONFIG = {
    "default_tasks": ["style", "test"],
    "verbosity": 2,
    "template": "{name:<10} {doc}",
}
PYTEST_VERBOSITY = "-v"  # Set as "", "-v", "-vv" or "-vvv"
MIN_COVERAGE = "50"  # Test fails if coverage is under this value
LINE_LENGHT = "79"  # black don't have a config file

# Set file_dep to this to run task only when the code changes
PYTHON_FILES = glob.glob("**/*.py", recursive=True)
BLACK_CMD = (
    "black -l "
    + LINE_LENGHT
    + r' {diff} --exclude "(\.venv|\.git|\{{ '{{' }}|\.tox|build|dist)" .'
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


def task__verchew():
    """Check system dependencies."""
    return {
        "file_dep": [".verchew.ini"],
        "actions": ["python bin/verchew --exit-code"]
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


# TODO
def task_launch():
    """Run the application entry point."""
    return {"actions": [show_task_doc]}
