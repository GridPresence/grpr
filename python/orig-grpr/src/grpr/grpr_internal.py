# -*- coding: utf-8 -*-
# Copyright TLM Partners, Inc. All Rights Reserved
"""
Generally useful stuff with potentially global scope
"""
import os
from typing import List
from pathlib import Path, PosixPath
from tlmcore.dockerdaemon import daemon_check
from tlmaws.configuration import AWSCredentials

IgorBotName: str = "tlmigorbot"


class DockerRunner:
    """
    Utility class for aggregating command line parameters for a
    docker run invocation.

    Cannot be instantiated unless a docker daemon is running on
    the host machine.
    """

    def __init__(
        self,
        name: str = IgorBotName,
        needs_aws: bool = False,
        needs_jfrog: bool = False,
    ) -> None:
        daemon_check()
        self._name = name
        self._home: Path = Path().home()
        self._pwd: Path = Path().cwd()
        self._volumes: List[str] = []
        self._envvars: List[str] = []
        self._runner: List[str] = []
        self._default_vols()
        if needs_aws is True:
            self._get_aws_creds()
        if needs_jfrog is True:
            self._get_jfrog_creds()

    def _default_vols(self) -> None:
        # This format will depend on the host OS
        host_work: str = str(Path().cwd())
        # This must be a Posix-style path for Linux
        mapped_work: str = str(PosixPath("/", "home", self._name, "work"))
        self.mapping(host=host_work, cont=mapped_work)

        # host_creds: str = f"{self._home}/{self._name}.credentials"
        # mapped_creds: str = f"/home/{self._name}/credentials"
        # self.mapping(host=host_creds, cont=mapped_creds)

    def _render(self) -> None:
        self._runner = []
        self._runner.append("docker")
        self._runner.append("run")
        self._runner.append("--rm")
        for vol in self._volumes:
            self._runner.append("-v")
            self._runner.append(vol)
        for envvar in self._envvars:
            self._runner.append("-e")
            self._runner.append(envvar)
        self._runner.append(self._name)

    def _get_aws_creds(self) -> None:
        creds: AWSCredentials = AWSCredentials()
        if "default" not in creds.sections:
            raise ValueError("No default AWS profile available")

        prf = creds.get_section("default")
        self.envvar(name="AWS_ACCESS_KEY_ID", val=prf["aws_access_key_id"])
        self.envvar(name="AWS_SECRET_ACCESS_KEY", val=prf["aws_secret_access_key"])
        self.envvar(name="AWS_SESSION_TOKEN", val=prf["aws_session_token"])

    def _get_jfrog_creds(self) -> None:
        self.envvar(name="JFROG_USER", val=os.environ["JFROG_USER"])
        self.envvar(name="JFROG_TOKEN", val=os.environ["JFROG_TOKEN"])
        self.envvar(name="JFROG_URL", val=os.environ["JFROG_URL"])

    def mapping(self, host: str, cont: str) -> None:
        """
        Utility method to add an additional volume mapping spec
        to the invocation.
        """
        self._volumes.append(f"{host}:{cont}")

    def envvar(self, name: str, val: str) -> None:
        """
        Utility method to insert an additional environment variable
        to the invocation.
        """
        self._envvars.append(f"{name}={val}")

    def __str__(self) -> str:
        self._render()
        return " ".join(self._runner)

    @property
    def runner(self) -> List[str]:
        """Accessor property for the run specification"""
        self._render()
        return self._runner
