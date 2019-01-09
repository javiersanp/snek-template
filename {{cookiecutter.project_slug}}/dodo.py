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
    """Initialize the repository and push first commit."""
    repo = "{{ cookiecutter.repository }}"
    return {
        "basename": "init-repo",
        "actions": [
            "git init",
            "git add .",
            'git commit -m "First commit"',
            "git remote add origin " + repo,
            "git  push -u origin master",
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
{% if cookiecutter.docs_generator == "Sphinx" %}    to_clean = [
        DOCS_HTML,
        os.path.join("docs", "api", "{{cookiecutter.project_slug}}*.rst"),
        os.path.join("docs", "api", "modules.rst"),
    ]
    apidoc_cmd = "poetry run sphinx-apidoc -o docs/apirm . {{ cookiecutter.project_slug }}"
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
    return {"basename": "serve-docs", "actions": [serve_cmd]}
{% else %}    return {
        "basename": "serve-docs",
        "task_dep": ["coverage:build", "docs:build"],
        "actions": ["poetry run mkdocs serve"],
    }
{% endif %}

# TODO
def task_launch():
    """Run the application entry point."""
    return {"actions": [show_task_doc]}
