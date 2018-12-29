"""Script for task automation.

See: http://pydoit.org/
"""
import glob

DOIT_CONFIG = {"default_tasks": ["task_check", "style"], "verbosity": 2}

PYTHON_FILES = glob.glob("**/*.py", recursive=True)


def get_subtask(action):
    """Return a dictionary defining a substack for 'action'."""
    return {
        "file_dep": PYTHON_FILES,
        "name": action.split(" ")[0],
        "actions": [action],
    }


def temp_task_install():
    """Install all dependencies in .venv virtual environment."""
    return {"file_dep": ["pyproject.toml"], "actions": ["poetry install"]}


def task_check():
    """Check diff of code formatters."""
    for action in ["black -l 79 --diff .", "isort --diff"]:
        yield {"name": action.split(" ")[0], "actions": [action]}


def task_format():
    """Run code formatters."""
    for action in ["black -l 79 .", "isort"]:
        yield get_subtask(action)


def task_style():
    """Check code styling."""
    for action in ["flake8", "pydocstyle", "isort --check-only -rc ."]:
        yield get_subtask(action)
