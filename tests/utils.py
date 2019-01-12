"""Utilities for tests."""

import json
import os
import subprocess
import sys
from contextlib import contextmanager

import pytest


@contextmanager
def inside_dir(dirpath):
    """
    Temporarily changes the current working directory and sys.path.

    :param dirpath: String, path of the directory to change
    """
    old_path = os.getcwd()
    try:
        os.chdir(str(dirpath))
        sys.path.insert(0, str(dirpath))
        yield
    finally:
        os.chdir(old_path)
        sys.path.pop(0)


@contextmanager
def poetryenv_in_project():
    """Temporarilly set poetry config to make virtualenvs in project."""
    venvset = "settings.virtualenvs.in-project"
    old_setting = subprocess.check_output(
        ["poetry", "config", venvset], universal_newlines=True
    ).strip("\n\r")
    try:
        subprocess.run(["poetry", "config", venvset, "true"])
        yield
    finally:
        subprocess.run(["poetry", "config", venvset, old_setting])


@pytest.fixture
def cookiecutter():
    with open("cookiecutter.json") as fo:
        vars_ = json.loads(fo.read())
        vars_["project_slug"] = (
            vars_["project_name"].lower().replace(" ", "_").replace("-", "_")
        )
        return vars_
