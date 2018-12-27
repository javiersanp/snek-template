import os
import shlex
import subprocess
from contextlib import contextmanager


@contextmanager
def inside_dir(dirpath):
    """
    Temporarily changes the current working directory.
    
    :param dirpath: String, path of the directory to change
    """
    print(dirpath)
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def command_exit_code(command):
    """
    Run a command and get the exit code.
    
    :param command: String with the command that will be executed
    :returns: Command exit code
    """
    return subprocess.check_call(shlex.split(command))


def test_bake_with_defaults(cookies):
    result = cookies.bake()
    assert result.exit_code == 0, "Exit code ok"
    assert result.exception is None, "Render without errors"
    assert result.project.isdir(), "Project directory exists"

    found_toplevel_files = [f.basename for f in result.project.listdir()]
    assert "your_project_name" in found_toplevel_files
    assert "tests" in found_toplevel_files


def test_slug(cookies):
    result = cookies.bake(extra_context={"project_name": "Foo Bar-Taz"})
    assert result.project.basename == "foo_bar_taz", "Test project slug"


def test_bake_and_run_tests(cookies):
    result = cookies.bake()
    with inside_dir(str(result.project)):
        assert command_exit_code("flake8") == 0, "Run code style check"
        assert command_exit_code("pytest") == 0, "Run tests ok"
        assert (
            command_exit_code("pydocstyle --ignore D104") == 0
        ), "Run docstring style check"
