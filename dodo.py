"""Script for task automation.

See: http://pydoit.org/
"""
import glob

DOIT_CONFIG = {"default_tasks": ["check", "style", "test"], "verbosity": 2}

PYTHON_FILES = [
    path for path in glob.iglob("**/*.py", recursive=True) if "{" not in path
]


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
    }


def task_check():
    """Check diff of code formatters."""
    black_cmd = (
        r'black -l 79 --diff --exclude "(\.venv|\.git|\{|\.tox|build|dist)" .'
    )
    for action in [black_cmd, "poetry run isort --diff"]:
        yield get_subtask(action, PYTHON_FILES)


def task_format():
    """Run code formatters."""
    black_cmd = r'black -l 79 --exclude "(\.venv|\.git|\{|\.tox|build|dist)" .'
    for action in [black_cmd, "poetry run isort -y"]:
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
    return {"actions": ["poetry run pytest"], "file_dep": PYTHON_FILES}
