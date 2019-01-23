"""Script for task automation.

See: http://pydoit.org/
Note: Install doit with python3, preferably in a virtual environment
"""
import glob
import os
import webbrowser
from contextlib import contextmanager
from subprocess import check_call, check_output
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


def get_stdout(command):
    """Run command with text capture and check, then return stdout."""
    return check_output(command, universal_newlines=True)


@contextmanager
def checkout(branch):
    """Temporarily checkout to branch."""
    current_branch = get_stdout(GIT_CURRENT_BRANCH_CMD).strip("\n\r ")
    try:
        check_call(["git", "checkout", branch])
        yield current_branch
    finally:
        check_call(["git", "checkout", current_branch])


def get_unstaged_changes():
    changes = get_stdout(GIT_UNSTAGED_CHANGES)
    if len(changes) > 0:
        print(changes)
    return changes


def check_diff(task):
    """
    Return updated if task param branch don't differ from current branch.
    
    First, validate the task param and if not valid pass the error to do_merge.
    """
    task.params_error = None
    branch = task.pos_arg_val[0] if len(task.pos_arg_val) > 0 else "master"
    branches = [
        branch_.strip("* \r")
        for branch_ in get_stdout(["git", "branch"]).strip("\n\r ").split("\n")
    ]
    current_branch = get_stdout(GIT_CURRENT_BRANCH_CMD).strip("\n\r ")
    if branch not in branches:
        task.params_error = "Branch {} don't exist.".format(branch)
    elif current_branch == branch:
        task.params_error = "Source and targets branch are the same."
    elif len(get_stdout(GIT_UNSTAGED_CHANGES)) > 0:
        task.params_error = "Git working directory is not clean."
    else:
        branch_diff = get_stdout(["git", "diff", "--name-only", branch])
        return len(branch_diff) == 0
    return False


def do_merge(task, pos_arg_val):
    """Merge current branch with given branch (default master) and push it."""
    if task.params_error is not None:
        return TaskFailed(task.params_error)
    branch = pos_arg_val[0] if len(pos_arg_val) > 0 else "master"
    with checkout(branch) as current_branch:
        check_call(["git", "merge", "--no-ff", current_branch])
        check_call(["git", "push", "origin", branch])


def do_release(pos_arg_val):
    """Bump version and push to master."""
    choices = ("major", "minor", "patch")
    if len(pos_arg_val) == 0:
        return TaskFailed(
            "Missing PART argument. Availlable choices are: {}.".format(
                str(choices)
            )
        )
    part = pos_arg_val[0]
    if part not in choices:
        return TaskFailed(
            "Wrong PART argument. Availlable choices are: {}.".format(
                str(choices)
            )
        )
    if len(get_stdout(GIT_UNSTAGED_CHANGES)) > 0:
        return TaskFailed("Git working directory is not clean.")
    with checkout("master"):
        if len(get_stdout(GIT_UNSTAGED_CHANGES)) > 0:
            return TaskFailed("Git working directory is not clean.")
        last_version = get_stdout(GIT_LAST_VERSION_CMD).strip("\n\r ")
        unreleased_commits = get_stdout(
            GIT_BRIEF_LOG_CMD + [last_version + ".."]
        )
        if len(unreleased_commits) > 0:
            print("Commits since", last_version)
            print(unreleased_commits)
        else:
            return TaskFailed("There aren't any commit to release.")
        check_call(["poetry", "run", "bump2version", "-n", "--verbose", part])
        proceed = input("Do you agree with the changes? (y/n): ")
        if proceed.lower().strip().startswith("y"):
            check_call(["poetry", "run", "bump2version", part])
            check_call(["git", "push", "--tags", "origin", "master"])
        else:
            return TaskFailed("Cancelled by user.")
    check_call(["git", "merge", "--no-ff", "master"])
    current_branch = get_stdout(GIT_CURRENT_BRANCH_CMD).strip("\n\r ")
    check_call(["git", "push", "origin", current_branch])


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
    return {
        "basename": "test-all",
        "task_dep": ["install"],
        "file_dep": PYTHON_FILES,
        "actions": ["poetry run tox"],
    }


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
    return {
        "basename": "serve-docs",
        "task_dep": ["install"],
        "actions": ["poetry run mkdocs serve"],
    }


# -------------------- Release ------------------------


def task_merge():
    """Merge current branch with given branch (default master) and push it."""
    return {
        "task_dep": ["test-all"],
        "pos_arg": "pos_arg_val",
        "uptodate": [check_diff],
        "actions": [do_merge],
    }


def task_release():
    """Bump the current version and release to the repository master branch."""
    return {
        "task_dep": ["test-all"],
        "pos_arg": "pos_arg_val",
        "actions": [do_release],
    }
