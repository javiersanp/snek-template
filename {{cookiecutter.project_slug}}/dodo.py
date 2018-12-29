"""Script for task automation.

See: http://pydoit.org/
"""
import glob

DOIT_CONFIG = {"default_tasks": ["task_check", "style"], "verbosity": 2}

PYTHON_FILES = glob.glob("**/*.py", recursive=True)


def get_subtask(cmd_action, file_dep=None):
    """Return a dictionary defining a substack for string 'cmd_action'."""
    task = {"name": cmd_action.split(" ")[0], "actions": [cmd_action]}
    if file_dep is not None:
        task["file_dep"] = file_dep
    return task


def temp_task_install():
    """Install all dependencies in .venv virtual environment."""
    return {"file_dep": ["pyproject.toml"], "actions": ["poetry install"]}


def task_check():
    """Check diff of code formatters."""
    for action in ["black -l 79 --diff .", "isort --diff"]:
        yield get_subtask(action, PYTHON_FILES)


def task_format():
    """Run code formatters."""
    for action in ["black -l 79 .", "isort"]:
        yield get_subtask(action)


def task_style():
    """Check code styling."""
    for action in ["flake8", "pydocstyle", "isort --check-only -rc ."]:
        yield get_subtask(action)
