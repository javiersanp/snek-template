import os
from subprocess import run

import pytest

import dodo
from tests.utils import inside_dir, poetryenv_in_project


def test_get_subtask_defaults():
    task = dodo.get_subtask("foo bar")
    assert task["name"] == "foo"
    assert task["actions"] == ["foo bar"]
    assert "file_dep" not in task


def test_get_subtask_with_file_dep():
    task = dodo.get_subtask("foo bar", "taz")
    assert task["name"] == "foo"
    assert task["actions"] == ["foo bar"]
    assert task["file_dep"] == "taz"


def test_get_subtask_with_poetry():
    task = dodo.get_subtask("poetry run foo bar")
    assert task["name"] == "foo"
    assert task["actions"] == ["poetry run foo bar"]


@pytest.mark.parametrize("command", ["format", "test"])
def test_doit_command_run_in_project(cookies, command):
    result = cookies.bake(extra_context={"project_name": "testing"})
    with inside_dir(str(result.project)):
        with poetryenv_in_project():
            assert run(["doit", command]).returncode == 0


def bad_style_code():
    return {
        "E111": """def myfunction():\n   pass\n""",
        "D400": """def myfunction():\n    \"\"\"Bla bla\"\"\"\n    pass\n""",
        "sorted": """import sys\nimport os\nprint(os.name, sys.platform)\n""",
    }


@pytest.mark.parametrize("pkg_name", ["mypackage", "tests"])
@pytest.mark.parametrize("expected_error", list(bad_style_code().keys()))
def test_doit_style_with_fails(cookies, capfd, pkg_name, expected_error):
    result = cookies.bake(extra_context={"project_name": "mypackage"})
    with inside_dir(str(result.project)):
        python_file = os.path.join(pkg_name, "dummy.py")
        with open(str(python_file), "w") as fo:
            fo.write(bad_style_code()[expected_error])
        with poetryenv_in_project():
            assert run(["doit", "style"]).returncode != 0
        captured = capfd.readouterr()
        assert expected_error in captured.out
