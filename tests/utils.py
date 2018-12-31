"""Utilities for tests."""

import os
import subprocess
from contextlib import contextmanager


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


@contextmanager
def poetryenv_in_project():
    """Temporarilly set poetry config to make virtualenvs in project."""
    venvset = "settings.virtualenvs.in-project"
    old_setting = subprocess.check_output(
        ["poetry", "config", venvset], text=True
    ).strip("\n\r")
    try:
        subprocess.run(["poetry", "config", venvset, "true"])
        yield
    finally:
        subprocess.run(["poetry", "config", venvset, old_setting])
