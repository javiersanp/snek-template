# -*- coding=utf-8 -*-
from click.testing import CliRunner

from {{cookiecutter.project_slug}} import cli


def test_emoji():
    runner = CliRunner()
    output = runner.invoke(cli.emoji, ["-e", "snek", "-c", "3"]).output
    assert output == u"🐍🐍🐍\n"
