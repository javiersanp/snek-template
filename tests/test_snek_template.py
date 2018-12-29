import json
import os
from contextlib import contextmanager
from subprocess import run

import pytest


@contextmanager
def inside_dir(dirpath):
    """
    Temporarily changes the current working directory.

    :param dirpath: String, path of the directory to change
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@pytest.fixture
def cookiecutter_vars():
    with open("cookiecutter.json") as fo:
        vars_ = json.loads(fo.read())
        vars_["project_slug"] = (
            vars_["project_name"].lower().replace(" ", "_").replace("-", "_")
        )
        return vars_


def test_bake_with_defaults(cookies, cookiecutter_vars):
    result = cookies.bake()
    assert result.exit_code == 0, "Exit code ok"
    assert result.exception is None, "Render without errors"
    assert result.project.isdir(), "Project directory exists"

    toplevel_files = [f.basename for f in result.project.listdir()]
    assert cookiecutter_vars["project_slug"] in toplevel_files
    assert "tests" in toplevel_files
    assert ".editorconfig" in toplevel_files
    assert ".gitignore" in toplevel_files
    assert "tox.ini" in toplevel_files
    assert ".verchew.ini" in toplevel_files


def test_slug(cookies):
    result = cookies.bake(extra_context={"project_name": "Foo Bar-Taz"})
    assert result.project.basename == "foo_bar_taz", "Test project slug"


def test_bake_and_run_tests(cookies):
    result = cookies.bake()
    with inside_dir(str(result.project)):
        assert run(["pytest"]).returncode == 0, "Run tests ok"


def test_doit_style_run_in_project(cookies):
    result = cookies.bake(extra_context={"project_name": "testing"})
    with inside_dir(str(result.project)):
        assert run(["doit", "style"]).returncode == 0, "Run doit style ok"


@pytest.mark.parametrize("pkg_name", ["mypackage", "tests"])
@pytest.mark.parametrize("expected_error", ["D400"])
def test_doit_style_with_fails(cookies, capfd, pkg_name, expected_error):
    bad_style_code = {
        "E111": """def myfunction():\n   pass\n""",
        "D400": """def myfunction():\n    \"\"\"Bla bla bla\"\"\"\n    pass\n""",
    }
    result = cookies.bake(extra_context={"project_name": "mypackage"})
    with inside_dir(str(result.project)):
        python_file = os.path.join(pkg_name, "dummy.py")
        with open(str(python_file), "w") as fo:
            fo.write(bad_style_code[expected_error])
        assert run(["cat", python_file])
        assert run(["doit", "style"]).returncode != 0
        captured = capfd.readouterr()
        assert expected_error in captured.out
