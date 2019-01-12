import importlib
from datetime import datetime
from subprocess import run

import mock
import pytest
from doit.cmd_base import ModuleTaskLoader
from doit.doit_cmd import DoitMain

import dodo
from tests.utils import inside_dir, poetryenv_in_project


def test_clean_paths(cookies):
    result = cookies.bake()
    project = result.project
    with inside_dir(project):
        importlib.reload(dodo)
        with mock.patch("dodo.os") as m_os:
            with mock.patch("dodo.glob") as m_glob:
                with mock.patch("dodo.shutil") as m_shutil:
                    m_glob.glob.side_effect = (("c", "d"), ("e", "f"))
                    m_os.path.isdir.side_effect = lambda path_: path_ > "c"
                    m_os.path.isfile.side_effect = lambda path_: path_ <= "c"
                    dodo.clean_paths("a", "b", "*", "?")
                    m_os.remove.assert_has_calls(
                        [mock.call("a"), mock.call("b"), mock.call("c")]
                    )
                    m_shutil.rmtree.assert_has_calls(
                        [mock.call("d"), mock.call("e"), mock.call("f")]
                    )
    importlib.reload(dodo)


def test_copy_directory(cookies):
    result = cookies.bake()
    project = result.project
    with inside_dir(project):
        importlib.reload(dodo)
        with mock.patch("dodo.os") as m_os:
            with mock.patch("dodo.shutil") as m_shutil:
                m_os.path.join = lambda *paths: "/".join(paths)
                m_os.path.basename.return_value = "b"
                m_os.path.isdir.side_effect = [True, True]
                m_os.path.exists.return_value = False
                dodo.copy_directory("a/b", "c")
                m_shutil.copytree.called_once_with("a/b", "c/b")


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
    result = cookies.bake()
    with inside_dir(result.project):
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
    with inside_dir(project):
        with project.join(pkg_name, "dummy.py").open("w") as fo:
            fo.write(bad_style_code()[expected_error])
        with poetryenv_in_project():
            assert run(["doit", "style"]).returncode != 0
        captured = capfd.readouterr()
        assert expected_error in captured.out


def test_doit_coverage(cookies):
    result = cookies.bake()
    with inside_dir(result.project):
        with poetryenv_in_project():
            importlib.reload(dodo)
            dodo.webbrowser = mock.MagicMock()
            assert DoitMain(ModuleTaskLoader(dodo)).run(["coverage"]) == 0
    importlib.reload(dodo)


@pytest.mark.parametrize("docs_generator", ["Sphinx", "MkDocs"])
def test_doit_docs(cookies, docs_generator):
    extra_context = {"docs_generator": docs_generator}
    result = cookies.bake(extra_context=extra_context)
    project = result.project
    with inside_dir(project):
        with poetryenv_in_project():
            importlib.reload(dodo)
            dodo.webbrowser = mock.MagicMock()
            project.mkdir("docs", "htmlcov")
            with project.join("docs", "htmlcov", "index.html").open("w") as fo:
                fo.write("")
            assert DoitMain(ModuleTaskLoader(dodo)).run(["docs"]) == 0
            assert project.join("site", "htmlcov").check(dir=1)
    importlib.reload(dodo)


def test_bumpversion(cookies):
    result = cookies.bake()
    with inside_dir(result.project):
        with poetryenv_in_project():
            run(["poetry", "install"])
            bump = run(
                ["poetry", "run", "bump2version", "patch", "-n", "--verbose"],
                capture_output=True,
                text=True,
            ).stderr
            assert '+version = "0.1.1"' in bump
            assert '+__version__ = "0.1.1"' in bump
            now = datetime.utcnow().strftime("%Y-%m-%d")
            assert (
                "+## [v0.1.1]({repo}/compare/0.1.0...0.1.1) ({now})".format(
                    repo="https://github.com/your_email/your_project_name".
                    now=now
                )
                in bump
            )
