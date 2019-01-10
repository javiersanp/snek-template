"""Script for task automation.

See: http://pydoit.org/
Note: Install doit with python3, preferably in a virtual environment
"""
import glob
import os
import webbrowser
from subprocess import run
from urllib.request import pathname2url

from doit.exceptions import TaskFailed

DOIT_CONFIG = {
    "default_tasks": ["format", "style", "test"],
    "verbosity": 2,
    "template": "{name:<10} {doc}",
}
LINE_LENGHT = "79"  # black don't have a config file

# Set file_dep to this to run task only when the code changes
PYTHON_FILES = [
    path for path in glob.iglob("**/*.py", recursive=True) if "{" not in path
]

# Set file_dep to this to run task only when the documentation changes
DOCS_FILES = (
    glob.glob("docs/**/*.md", recursive=True)
    + glob.glob("**/*.md")
    + ["{{cookiecutter.project_slug}}/docs/tasks.md"]
)

BLACK_CMD = (
    "black -l "
    + LINE_LENGHT
    + r' {diff} --exclude "(\.venv|\.git|\{{|\.tox|build|dist)" .'
)
COV_HTML = os.path.join("docs", "htmlcov")
COV_INDEX = os.path.join(COV_HTML, "index.html")
DOCS_HTML = "site"
DOCS_INDEX = os.path.join(DOCS_HTML, "index.html")
VERCHEW = os.path.join("bin", "verchew")
GIT_LAST_VERSION_CMD = ["git", "describe", "--tags", "--abbrev=0"]
GIT_BRIEF_LOG_CMD = ["git", "--no-pager", "log", "--oneline"]
GIT_UNSTAGED_CHANGES = ["git", "status", "--porcelain", "--untracked=no"]
GIT_CURRENT_BRANCH_CMD = ["git", "rev-parse", "--abbrev-ref", "HEAD"]


# --------------------- Actions ------------------------


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


def get_stdout(command):
    """Run command with text capture and check, then return stdout."""
    return run(
        command, capture_output=True, universal_newlines=True, check=True
    ).stdout


def do_merge(branch):
    """Merge current branch with given branch (default master) and push it."""
    current_branch = get_stdout(GIT_CURRENT_BRANCH_CMD)
    if current_branch == branch:
        return TaskFailed("Source and targets branch are the same.")
    changes = get_stdout(GIT_UNSTAGED_CHANGES)
    if len(changes.stdout) > 0:
        return TaskFailed("Git working directory is not clean.")
    run(["git", "checkout", branch], check=True)
    run(["git", "merge", "-no-ff", current_branch], check=True)
    run(["git", "push", "origin", branch], check=True)
    run(["git", "checkout", current_branch], check=True)


def do_release(part):
    """Bump version and push to master."""
    run(["git", "checkout", "master"], check=True)
    changes = get_stdout(GIT_UNSTAGED_CHANGES)
    if len(changes.stdout) > 0:
        return TaskFailed("Git working directory is not clean.")
    last_version = get_stdout(GIT_LAST_VERSION_CMD).strip("\n\r ")
    unreleased_commits = get_stdout(GIT_BRIEF_LOG_CMD + [last_version + ".."])
    if len(unreleased_commits) > 0:
        print("Commits since", last_version)
        print(unreleased_commits)
    else:
        return TaskFailed("There aren't any commit to release.")
    run(["poetry", "run", "bump2version", "-n", "--verbose", part], check=True)
    proceed = input("Do you agree with the changes? (y/n): ")
    if proceed.lower().strip().startswith("y"):
        run(["poetry", "run", "bump2version", part], check=True)
        run(["git", "push", "origin", "master"], check=True)
    else:
        return TaskFailed("Cancelled by user.")


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
    return {
        "task_dep": ["install"],
        "file_dep": PYTHON_FILES,
        "actions": ["poetry run pytest"],
    }


def task_test_all():
    """Run tests with tox using different Python versions."""
    return {"basename": "test-all", "actions": ["tox"]}


def task_coverage():
    """Generate and show the coverage html report."""
    yield {
        "name": "build",
        "task_dep": ["test"],
        "file_dep": [".coverage"],
        "actions": ["poetry run coverage html"],
        "targets": [COV_HTML, COV_INDEX],
    }
    yield {
        "name": "show",
        "task_dep": ["coverage:build"],
        "actions": [(open_in_browser, (COV_INDEX,))],
    }


def task_docs():
    """Generate and show the HTML documentation."""
    yield {
        "name": "build",
        "task_dep": ["install"],
        "file_dep": DOCS_FILES,
        "actions": ["poetry run mkdocs build"],
        "targets": [DOCS_HTML, DOCS_INDEX],
    }
    yield {
        "name": "show",
        "task_dep": ["docs:build"],
        "actions": [(open_in_browser, (DOCS_INDEX,))],
    }


def task_serve_docs():
    """Show the documentation and coverage watching for changes."""
    return {"basename": "serve-docs", "actions": ["poetry run mkdocs serve"]}


# -------------------- Release ------------------------


def task_merge():
    """Merge current branch with given branch (default master) and push it."""
    return {
        # "task_dep": ["test-all"],
        "params": [
            {
                "name": "branch",
                "long": "branch",
                "short": "b",
                "default": "master",
                "help": "Branch to merge into.",
            }
        ],
        "actions": [do_merge],
    }


def task_release():
    """Bump the current version and release to the repository master branch."""
    return {
        "task_dep": ["test-all"],
        "params": [
            {
                "name": "part",
                "long": "part",
                "short": "p",
                "choices": (("major", ""), ("minor", ""), ("patch", "")),
                "default": "patch",
                "help": "The part of the version to increase.",
            }
        ],
        "actions": [do_release],
    }


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
