# -*- coding: utf-8 -*-
# Copyright TLM Partners, Inc. All Rights Reserved
"""
Command execution environment for CLI apps in Python
"""
import typer

from . import python, docker, util, __version__


def version_callback(value: bool):
    """
    The version callback method
    """
    if value:
        typer.echo(f"CLI (grpr) Version: {__version__}\n")
        #typer.echo("Comprising:")
        #typer.echo(f"       grpr: {__version__}")
        raise typer.Exit()


app = typer.Typer(add_completion=False)


# pylint: disable=unused-argument
@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        help="Display current installed version",
    ),
):
    """
    The Grpr toolkit.

    Implements automation for repetitive development use cases.
    """

app.add_typer(docker.app, name="iac", help="Infrastructure-as-Code development tools")
app.add_typer(python.app, name="py", help="Python package and module development tools")
app.add_typer(util.app, name="util", help="General utilities")


def main():
    """
    Entry point
    """
    app()


if __name__ == "__main__":
    typer.run(main)
