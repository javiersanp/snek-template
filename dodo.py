"""Script for task automation.

See: http://pydoit.org/
"""
import glob

DOIT_CONFIG = {"default_tasks": ["task_check", "style"], "verbosity": 2}

PYTHON_FILES = [
    path for path in glob.iglob("**/*.py", recursive=True) if "{" not in path
]


def get_subtask(cmd_action, file_dep=None):
    """Return a dictionary defining a substack for string 'cmd_action'."""
    task = {"name": cmd_action.split(" ")[0], "actions": [cmd_action]}
    if file_dep is not None:
        task["file_dep"] = file_dep
    return task


def task_verchew():
    """Check system dependencies"""
    return {
        "file_dep": [".verchew.ini"],
        "actions": ["python bin/verchew --exit-code"],
        "verbosity": 0,
    }


def task_install():
    """Install all dependencies in a virtual environment."""
    return {
        "file_dep": ["pyproject.toml"],
        "actions": ["poetry install"],
        "task_dep": ["verchew"],
        "verbosity": 1,
    }


def task_check():
    """Check diff of code formatters."""
    black_cmd = (
        r'black -l 79 --diff --exclude "(\.venv|\.git|\{|\.tox|build|dist)" .'
    )
    for action in [black_cmd, "isort --diff"]:
        yield get_subtask(action)


def task_format():
    """Run code formatters."""
    black_cmd = r'black -l 79 --exclude "(\.venv|\.git|\{|\.tox|build|dist)" .'
    for action in [black_cmd, "isort"]:
        yield get_subtask(action, PYTHON_FILES)


def task_style():
    """Check code styling."""
    for action in ["flake8", "pydocstyle", "isort --check-only -rc ."]:
        yield get_subtask(action, PYTHON_FILES)
