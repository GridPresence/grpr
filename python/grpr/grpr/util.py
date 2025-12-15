# -*- coding: utf-8 -*-
# Copyright TLM Partners, Inc. All Rights Reserved
"""
Subcommand set related to general utility functions
"""
import os
import uuid
from typing import List, Dict
from pathlib import Path
import typer
from tlmcore.shellcmd import TLMShellCmd
from tlmcore.json import TLMJson
from .util_internal import PipConf, PyPiRc, TerraformCredential

app = typer.Typer()


@app.command()
def config_local():
    """
    Create the relevant local configurations necessary to use the TLM
    JFrog Artifactory as the one-source of truth for each package type.
    """
    jfuser: str = os.environ["JFROG_USER"]
    jftoken: str = os.environ["JFROG_TOKEN"]
    jfurl: str = os.environ["JFROG_URL"]
    # PyPi configurations
    npipconf: PipConf = PipConf()
    npipconf.update(user=jfuser, token=jftoken, url=jfurl)
    npipconf.close()
    npypirc: PyPiRc = PyPiRc()
    npypirc.update(user=jfuser, token=jftoken, url=jfurl)
    npypirc.close()
    tfcred: TerraformCredential = TerraformCredential()
    tfcred.update(token=jftoken, url=jfurl)


@app.command()
def gen_uuid(
    num: int = typer.Argument(1, help="Number of UUIDs to generate"),
    jout: bool = typer.Option(False, help="Format output as JSON"),
):
    """
    Create one or more simple random UUIDs (type 4, as per RFC 4122)
    """
    output: List[str] = []
    # Don't worry about unused count variable
    # pylint: disable=unused-variable
    for count in range(0, num):
        target = uuid.uuid4()
        output.append(str(target))
    if jout:
        retval: Dict[str, List[str]] = {}
        retval["uuids"] = output
        print(TLMJson(struct=retval))
    else:
        for entry in output:
            print(entry)


def substitute_in(filename: Path, pattern: str, value: str, implement: bool):
    """PLACEHOLDER"""
    # Safely read the input filename using 'with'
    with open(filename, encoding="utf8") as fyle:
        source = fyle.read()
        if pattern not in source:
            return
        # Show path to file that will be changed
        print(f"\t-\t{filename}")
    # If we have decided to write the changes
    if implement is True:
        # Safely write the changed content wherever it is found in the file
        with open(filename, "w", encoding="utf8") as fyle:
            source = source.replace(pattern, value)
            fyle.write(source)


@app.command()
def sub_env(
    name: str,
    suffix: str = typer.Argument("tf", help="File suffix to target"),
    recurse: bool = typer.Option(
        False, help="Recursively substitute in subdirectories"
    ),
    write: bool = typer.Option(False, help="Write the change."),
):
    """
    Substitute all occurences of a named string with the corresponding environment variable value.
    """
    envar = f"{os.getenv(name)}"
    regexp = f"*.{suffix}"
    # Visual feedback
    print(f"{name} = {envar}")
    # Extend the glob pattern if we are including subdirectories
    if recurse is True:
        regexp = f"**/*.{suffix}"
    # Create the list of matching entries
    candidates = Path(".").glob(regexp)
    # Only include valid files
    files = [x for x in candidates if x.is_file()]
    # Run each of the candidate files through the substitution logic
    for item in files:
        substitute_in(filename=item, pattern=name, value=envar, implement=write)


@app.command()
def upgrade_self(
    jout: bool = typer.Option(False, help="Format output as JSON")
) -> None:
    """
    Upgrade all the igor dependencies in the local environment
    """
    deps: List[str] = ["tlmcore", "tlmaws", "tlmigor"]
    cmd: List[str] = ["python3", "-m", "pip", "install", "--upgrade"]
    cmd.extend(deps)
    execute: TLMShellCmd = TLMShellCmd(cspec=cmd, capture=jout)
    if jout:
        print(execute)
