import importlib
from subprocess import run

import mock
import pytest
from doit.cmd_base import ModuleTaskLoader
from doit.doit_cmd import DoitMain

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


@pytest.mark.parametrize("command", ["format", "style", "test"])
def test_doit_command_run_in_project(cookies, command):
    result = cookies.bake(extra_context={"project_name": "testing"})
    print(str(result.project))
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
    project = result.project
    with inside_dir(str(project)):
        with project.join(pkg_name, "dummy.py").open("w") as fo:
            fo.write(bad_style_code()[expected_error])
        with poetryenv_in_project():
            assert run(["doit", "style"]).returncode != 0
        captured = capfd.readouterr()
        assert expected_error in captured.out


def test_doit_coverage(cookies):
    result = cookies.bake(extra_context={"project_name": "testing"})
    with inside_dir(str(result.project)):
        with poetryenv_in_project():
            importlib.reload(dodo)
            dodo.webbrowser = mock.MagicMock()
            assert DoitMain(ModuleTaskLoader(dodo)).run(["coverage"]) == 0
    importlib.reload(dodo)


@pytest.mark.parametrize("docs_generator", ["Sphinx", "MkDocs"])
def test_doit_docs(cookies, docs_generator):
    result = cookies.bake(extra_context={"docs_generator": docs_generator})
    project = result.project
    with inside_dir(str(project)):
        with poetryenv_in_project():
            importlib.reload(dodo)
            dodo.webbrowser = mock.MagicMock()
            project.mkdir("docs", "htmlcov")
            with project.join("docs", "htmlcov", "index.html").open("w") as fo:
                fo.write("")
            assert DoitMain(ModuleTaskLoader(dodo)).run(["docs"]) == 0
            assert project.join("site", "htmlcov").check(dir=1)
    importlib.reload(dodo)
