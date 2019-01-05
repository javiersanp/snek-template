"""Script for task automation.

See: http://pydoit.org/
Note: Install doit with python3, preferably in a virtual environment
"""
import glob
import os
import shutil
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

# Set file_dep to this to run task only when the documentation changes
DOCS_FILES = (
    glob.glob("docs/**/*.md", recursive=True)
    + glob.glob("docs/**/*.rst", recursive=True)
    + glob.glob("**/*.md")
    + glob.glob("**/*.rst")
)

BLACK_CMD = (
    "black -l "
    + LINE_LENGHT
    + r' {diff} --exclude "(\.venv|\.git|\{{ '{{' }}|\.tox|build|dist)" .'
)
COV_HTML = os.path.join("docs", "htmlcov")
COV_INDEX = os.path.join(COV_HTML, "index.html")
DOCS_HTML = "site"
DOCS_INDEX = os.path.join(DOCS_HTML, "index.html")
VERCHEW = os.path.join("bin", "verchew")


# --------------------- Actions ------------------------


def clean_directories(*args):
    """Delete the given directories."""
    for folder in args:
        if os.path.isdir(folder):
            print("Cleaning ", folder)
            shutil.rmtree(folder)


def copy_directory(source_dir, target_dir):
    """Copy source directory into target directory."""
    target = os.path.join(target_dir, os.path.basename(source_dir))
    if (
        os.path.isdir(source_dir)
        and os.path.isdir(target_dir)
        and not os.path.exists(target)
    ):
        shutil.copytree(source_dir, target)


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


# ------------------- Installation ---------------------


def task__verchew():
    """Check system dependencies."""
    return {
        "file_dep": [".verchew.ini"],
        "actions": ["python {} --exit-code".format(VERCHEW)],
    }


def task_install():
    """Install all dependencies in a virtual environment."""
    return {
        "file_dep": ["pyproject.toml"],
        "actions": ["poetry install"],
        "task_dep": ["_verchew"],
        "targets": ["poetry.lock"],
    }


# --------------------- Development ----------------------


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
    return {
        "task_dep": ["install"],
        "file_dep": PYTHON_FILES,
        "actions": [pytest_cmd],
    }


def task__covhtml():
    return {
        "task_dep": ["install"],
        "file_dep": [".coverage"],
        "actions": ["poetry run coverage html"],
        "targets": [COV_HTML, COV_INDEX],
    }


def task_coverage():
    """Generate and show the coverage html report."""
    return {
        "actions": [(open_in_browser, (COV_INDEX,))],
        "task_dep": ["test", "_covhtml"],
    }


{% if cookiecutter.docs_generator == "Sphinx" %}def task__docshtml():
    return {
        "task_dep": ["install"],
        "file_dep": DOCS_FILES,
        "actions": [
            (clean_directories, (DOCS_HTML,)),
            "poetry run sphinx-build -b html -j auto -a docs site",
            (copy_directory, (os.path.join("docs", "htmlcov"), DOCS_HTML)),
        ],
        "targets": [DOCS_HTML, DOCS_INDEX],
        "clean": [(clean_directories, (DOCS_HTML,))],
    }


{% else %}def task__docshtml():
    return {
        "task_dep": ["install"],
        "file_dep": DOCS_FILES,
        "actions": ["poetry run mkdocs build"],
        "targets": [DOCS_HTML, DOCS_INDEX],
    }


{% endif %}def task_docs():
    """Generate and show the HTML documentation."""
    return {
        "actions": [(open_in_browser, (DOCS_INDEX,))],
        "task_dep": ["_docshtml"],
    }


# TODO
def task_launch():
    """Run the application entry point."""
    return {"actions": [show_task_doc]}
