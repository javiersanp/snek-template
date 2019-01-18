# -*- coding=utf-8 -*-
"""Command Line Interface for {{cookiecutter.project_name}}."""

from __future__ import absolute_import

import sys

import click

from {{cookiecutter.project_slug}}.{{cookiecutter.project_slug}} import get_emojis


@click.command()
@click.option(
    "-e",
    "--emoji",
    required=True,
    type=click.Choice(get_emojis().keys()),
    help="The emoji to show.",
)
@click.option("-c", "--count", default=1, help="Number of emojis.")
def emoji(emoji, count=1):
    click.echo(get_emojis()[emoji] * count)


if __name__ == "__main__":
    sys.exit(emoji())
