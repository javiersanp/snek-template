import datetime
import json

import pytest

from tests.utils import inside_dir


@pytest.fixture
def cookiecutter():
    with open("cookiecutter.json") as fo:
        vars_ = json.loads(fo.read())
        vars_["project_slug"] = (
            vars_["project_name"].lower().replace(" ", "_").replace("-", "_")
        )
        return vars_


def test_with_defaults(cookies, cookiecutter):
    result = cookies.bake()
    assert result.exit_code == 0, "Exit code ok"
    assert result.exception is None, "Render without errors"
    assert result.project.isdir(), "Project directory exists"

    toplevel_files = [f.basename for f in result.project.listdir()]
    assert cookiecutter["project_slug"] in toplevel_files
    assert "tests" in toplevel_files
    assert ".editorconfig" in toplevel_files
    assert ".gitignore" in toplevel_files
    assert "tox.ini" in toplevel_files
    assert ".verchew.ini" in toplevel_files
    assert "extra_context.j2" not in toplevel_files


def test_slug(cookies):
    result = cookies.bake(extra_context={"project_name": "Foo Bar-Taz"})
    assert result.project.basename == "foo_bar_taz", "Test project slug"


def license_strings():
    return {
        "MIT": "Permission is hereby granted, free of charge",
        "BSD-4-Clause": "Redistribution and use in source and binary forms",
        "Apache-2.0": "Licensed under the Apache License, Version 2.0",
        "GPL-3.0": "GNU GENERAL PUBLIC LICENSE",
    }


@pytest.mark.parametrize(
    "license, target_string", list(license_strings().items())
)
def test_selecting_license(cookies, cookiecutter, license, target_string):
    result = cookies.bake(extra_context={"license": license})
    with inside_dir(str(result.project)):
        license_text = result.project.join("LICENSE").read()
        assert target_string in license_text
        if license != "GPL-3.0":
            assert str(datetime.datetime.now().year) in license_text
            assert cookiecutter["full_name"] in license_text
        pyproject = result.project.join("pyproject.toml").read()
        assert license in pyproject


def test_not_open_source_license(cookies):
    result = cookies.bake(extra_context={"license": "Not open source"})
    with inside_dir(str(result.project)):
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "LICENSE" not in found_toplevel_files


def test_pyproject(cookies, cookiecutter):
    result = cookies.bake()
    with inside_dir(str(result.project)):
        pyproject = result.project.join("pyproject.toml").read()
        assert cookiecutter["project_slug"] in pyproject
        assert cookiecutter["version"] in pyproject
        assert cookiecutter["project_short_description"] in pyproject
        assert cookiecutter["full_name"] in pyproject
        assert cookiecutter["email"] in pyproject
