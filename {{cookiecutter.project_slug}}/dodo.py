"""Script for task automation.

See: http://pydoit.org/
Note: Install doit with python3, preferably in a virtual environment
"""
import glob
import os
import shutil
import webbrowser
from subprocess import check_call, check_output
from urllib.request import pathname2url

from doit.exceptions import TaskFailed

DOIT_CONFIG = {
    "default_tasks": ["style", "test"],
    "verbosity": 2,
    "template": "{name:<10} {doc}",
}
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
GIT_LAST_VERSION_CMD = ["git", "describe", "--tags", "--abbrev=0"]
GIT_BRIEF_LOG_CMD = ["git", "--no-pager", "log", "--oneline"]
GIT_UNSTAGED_CHANGES = ["git", "status", "--porcelain", "--untracked=no"]
GIT_CURRENT_BRANCH_CMD = ["git", "rev-parse", "--abbrev-ref", "HEAD"]


# --------------------- Actions ------------------------


def clean_paths(*args):
    """
    Delete the given paths (files or directories).

    Can contain shell-style wildcards.
    """
    paths = []
    for path_ in args:
        if "*" in path_ or "?" in path_:
            paths.extend(glob.glob(path_))
        else:
            paths.append(path_)
    for path_ in paths:
        if os.path.isdir(path_):
            shutil.rmtree(path_)
        elif os.path.isfile(path_):
            os.remove(path_)


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


def targets_exists(task):
    """Return True (updated) if all task targets exists."""
    return all([os.path.exists(target) for target in task.targets])


def get_stdout(command):
    """Run command with text capture and check, then return stdout."""
    return check_output(command, universal_newlines=True)


def do_merge(branch):
    """Merge current branch with given branch (default master) and push it."""
    branches = [
        branch_.strip("* \r")
        for branch_ in get_stdout(["git", "branch"]).strip("\n\r ").split("\n")
    ]
    if branch not in branches:
        return TaskFailed("Branch {} don't exist.".format(branch))
    current_branch = get_stdout(GIT_CURRENT_BRANCH_CMD).strip("\n\r ")
    if current_branch == branch:
        return TaskFailed("Source and targets branch are the same.")
    changes = get_stdout(GIT_UNSTAGED_CHANGES)
    if len(changes) > 0:
        print(changes)
        return TaskFailed("Git working directory is not clean.")
    check_call(["git", "checkout", branch])
    check_call(["git", "merge", "--no-ff", current_branch])
    check_call(["git", "push", "origin", branch])
    check_call(["git", "checkout", current_branch])


def do_release(part):
    """Bump version and push to master."""
    current_branch = get_stdout(GIT_CURRENT_BRANCH_CMD).strip("\n\r ")
    check_call(["git", "checkout", "master"])
    changes = get_stdout(GIT_UNSTAGED_CHANGES)
    if len(changes) > 0:
        return TaskFailed("Git working directory is not clean.")
    last_version = get_stdout(GIT_LAST_VERSION_CMD).strip("\n\r ")
    unreleased_commits = get_stdout(GIT_BRIEF_LOG_CMD + [last_version + ".."])
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
        check_call(["git", "checkout", current_branch])
        return TaskFailed("Cancelled by user.")
    check_call(["git", "checkout", current_branch])


def show_task_doc(task):
    print("TODO: " + task.doc)


# ------------------- Installation ---------------------


def task__verchew():
    """Check system dependencies."""
    return {
        "file_dep": [".verchew.ini"],
        "actions": ["python {} --exit-code".format(VERCHEW)],
    }


def task_init_repo():
    """
    Initialize the repository and push first commit.

    Create a empty local git, connect it to the remote repository, tag the
    initial version, push all files to the `master` branch, create the
    `develop` branch and checkout to it.
    """
    repo = "{{ cookiecutter.repository }}"
    return {
        "basename": "init-repo",
        "actions": [
            "git init",
            "git add .",
            'git commit -m "First commit"',
            "git remote add origin " + repo,
            "git tag v{{ cookiecutter.version }}",
            "git push -u --tags origin master",
            "git checkout -b develop",
        ],
        "targets": [".git"],
        "uptodate": [targets_exists],
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
        "actions": ["poetry run pytest --cov --cov-config=tox.ini"],
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
{% if cookiecutter.docs_generator == "Sphinx" %}    to_clean = [
        DOCS_HTML,
        os.path.join("docs", "api", "{{cookiecutter.project_slug}}*.rst"),
        os.path.join("docs", "api", "modules.rst"),
    ]
    apidoc_cmd = "poetry run sphinx-apidoc -o docs/api {{ cookiecutter.project_slug }}"
    yield {
        "name": "build",
        "task_dep": ["install"],
        "file_dep": DOCS_FILES,
        "actions": [
            (clean_paths, to_clean),
            apidoc_cmd,
            "poetry run sphinx-build -b html -j auto -a docs site",
            (copy_directory, (os.path.join("docs", "htmlcov"), DOCS_HTML)),
        ],
        "targets": [DOCS_HTML, DOCS_INDEX],
        "clean": [(clean_paths, to_clean)],
{% else %}    yield {
        "name": "build",
        "task_dep": ["install"],
        "file_dep": DOCS_FILES,
        "actions": ["poetry run mkdocs build"],
        "targets": [DOCS_HTML, DOCS_INDEX],
{% endif %}    }
    yield {
        "name": "show",
        "task_dep": ["docs:build"],
        "actions": [(open_in_browser, (DOCS_INDEX,))],
    }


def task_serve_docs():
    """Show the documentation and coverage watching for changes."""
{% if cookiecutter.docs_generator == "Sphinx" %}    serve_docs = os.path.join("bin", "serve-docs")
    serve_cmd = "poetry run python " + serve_docs
    return {
        "basename": "serve-docs",
        "task_dep": ["coverage:build", "docs:build"],
        "actions": [serve_cmd],
    }
{% else %}    return {
        "basename": "serve-docs",
        "task_dep": ["install"],
        "actions": ["poetry run mkdocs serve"],
    }
{% endif %}

# -------------------- Release ------------------------


def task_merge():
    """Merge current branch with given branch (default master) and push it."""
    return {
        "task_dep": ["init-repo", "test-all"],
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
        "task_dep": ["init-repo", "test-all"],
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
def task_launch():
    """Run the application entry point."""
    return {"actions": [show_task_doc]}
