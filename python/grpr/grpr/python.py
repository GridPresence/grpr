# -*- coding: utf-8 -*-
# Copyright TLM Partners, Inc. All Rights Reserved
"""
Subcommand set related to the creation and maintenance of Python packages
"""
from typing import List, Dict
import typer
from tlmcore.shellcmd import TLMShellCmd
from tlmcore.json import TLMJson
from tlmaws.configuration import AWSCredentials
from .grpr_internal import DockerRunner
from .python_internal import PypiVersion, PythonPackage

app = typer.Typer()


@app.command()
def check(
    name: str, jout: bool = typer.Option(False, help="Format output as JSON")
) -> None:
    """
    Validate and test that a Python package can be deployed.
    """
    container = DockerRunner(needs_jfrog=True, needs_aws=True)
    container.envvar(name="TARGET_PACKAGE", val=name)
    container.envvar(name="IGOR_PY", val="1")
    execute: TLMShellCmd = TLMShellCmd(cspec=container.runner, capture=jout)
    if jout:
        print(execute)


@app.command()
def deploy(
    name: str, jout: bool = typer.Option(False, help="Format output as JSON")
) -> None:
    """
    Deploy a versioned package into a PyPi repository.
    """
    container = DockerRunner(needs_jfrog=True)
    container.envvar(name="TARGET_PACKAGE", val=name)
    container.envvar(name="IGOR_PY", val="1")
    container.envvar(name="DEPLOY_CHANGES", val="1")
    # If we try to deploy documentation at the company level, we will
    # need access to the destination endpoint.
    creds: AWSCredentials = AWSCredentials()
    if "techopsdocs" in creds.sections:
        topsdox = creds.get_section("techopsdocs")
        container.envvar(
            name="TOPSDOX_AWS_ACCESS_KEY_ID", val=topsdox["aws_access_key_id"]
        )
        container.envvar(
            name="TOPSDOX_AWS_SECRET_ACCESS_KEY",
            val=topsdox["aws_secret_access_key"],
        )
    execute: TLMShellCmd = TLMShellCmd(cspec=container.runner, capture=jout)
    if jout:
        print(execute)


@app.command()
def create_pkg(name: str) -> None:
    """
    Create a new Python package source directory tree
    """
    # It's a resource that creates a package subdirectory on instantiation
    # The object is never used again
    # pylint: disable=unused-variable
    ppkg: PythonPackage = PythonPackage(name=name)


# @app.command()
# def create_mod(name: str, package: str) -> None:
#    """
#    Create a new Python module in a package source directory tree
#    """
# It's a resource that creates a new source module on instantiation
# The object is never used again
# pylint: disable=unused-variable
#   pmodule: PythonModule = PythonModule(name=name, pkg=package)


@app.command()
def vnum_plus(
    name: str,
    level: str = typer.Argument(
        "patch", help="Increment level: 'patch', 'minor' or 'major'"
    ),
    jout: bool = typer.Option(False, help="Format output as JSON"),
) -> None:
    """
    Generate the next valid version digit string for the named package according
    to the applied patch level.
    """
    # Reminder: refactor this
    # pylint: disable=duplicate-code
    pversion: PypiVersion = PypiVersion(name=name, level=level)
    if jout:
        temp: Dict[str, str] = {"Version": pversion.new_version}
        print(TLMJson(struct=temp))
    else:
        print(pversion.new_version)


@app.command()
def vnum(
    name: str, jout: bool = typer.Option(False, help="Format output as JSON")
) -> None:
    """
    Get the currently deployed version digit string for the named package
    """
    # Reminder: refactor this
    # pylint: disable=duplicate-code
    pversion: PypiVersion = PypiVersion(name=name)
    if jout:
        temp: Dict[str, str] = {"Version": pversion.version}
        print(TLMJson(struct=temp))
    else:
        print(pversion.version)


@app.command()
def sync(jout: bool = typer.Option(False, help="Format output as JSON")) -> None:
    """
    Upgrade all the package dependencies in the local environment
    """
    cmd: List[str] = [
        "python3",
        "-m",
        "pip",
        "install",
        "--upgrade",
    ]
    with open("requirements.txt", encoding="utf-8") as reqs:
        for req in reqs:
            cmd.append(req)
    execute: TLMShellCmd = TLMShellCmd(cspec=cmd, capture=jout)
    if jout:
        print(execute)


if __name__ == "__main__":
    app()
