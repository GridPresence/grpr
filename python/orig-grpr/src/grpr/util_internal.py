# -*- coding: utf-8 -*-
# Copyright TLM Partners, Inc. All Rights Reserved
"""
Support structures for general utility functions
"""
from typing import Dict, Any
from pathlib import Path
from tlmcore.inifile import IniFile
from tlmcore.oscheck import is_windows
from tlmcore.json import TLMJson


# pylint: disable=too-few-public-methods
class PipConf(IniFile):
    """
    An abstraction for manipulating the local pip.conf (or pip.ini) file in order to
    generate the credentials for pip to access the TLM Artifactory Pypi repository.
    """

    def __init__(self):
        home: Path = Path().home()
        # Windows is an outlier
        if is_windows() is True:
            pipdir = Path(home).joinpath("pip")
        else:
            pipdir = Path(home).joinpath(".config", "pip")
        # Ensure the directory is created if it doesn't already exist
        pipdir.mkdir(parents=True, exist_ok=True)
        # Windows is an outlier here too
        if is_windows() is True:
            self._pipconf = Path(pipdir).joinpath("pip.ini")
        else:
            self._pipconf = Path(pipdir).joinpath("pip.conf")
        # Ensure the file is created if it doesn't already exist
        self._pipconf.touch(exist_ok=True)
        super().__init__(name=self._pipconf)

    def update(self, user: str, token: str, url: str) -> None:
        """
        This method updates the global section with the TLM-specific index-url
        generated from the components passed in the invocation.
        """
        https: str = "https://"
        suffix: str = "artifactory/api/pypi/pypi/simple"
        if not self.has_section("global"):
            self.add_section("global")
        glob = self.get_section("global")
        index_url = f"{https}{user}:{token}@{url}/{suffix}"
        glob["index-url"] = index_url


# pylint: disable=too-few-public-methods
class PyPiRc(IniFile):
    """
    An abstraction for manipulating the local .pypirc file in order to generate the
    credentials for twine to access the TLM Artifactory Pypi repository.
    """

    def __init__(self):
        home: Path = Path().home()
        # This is universal on all platforms
        self._pypirc = Path(home).joinpath(".pypirc")
        # Ensure the file is created if it doesn't already exist
        self._pypirc.touch(exist_ok=True)
        super().__init__(name=self._pypirc)

    def update(self, user: str, token: str, url: str):
        """
        This method updates the distutils and local sections with the TLM-specific
        credentials generated from the components passed in the invocation.
        """
        https: str = "https://"
        suffix: str = "artifactory/api/pypi/pypi"
        if not self.has_section("distutils"):
            self.add_section("distutils")
        distutils = self.get_section("distutils")
        distutils["index-servers"] = "local"
        if not self.has_section("local"):
            self.add_section("local")
        local = self.get_section("local")
        local["repository"] = f"{https}{url}/{suffix}"
        local["username"] = user
        local["password"] = token


class TerraformCredential:
    """
    An abstraction for maintainming a credential suitable for use when
    accessing a private Terraform module repository.
    """

    def __init__(self):
        home: Path = Path().home()
        tfdir = Path(home).joinpath(".terraform.d")
        tfdir.mkdir(parents=True, exist_ok=True)
        self._creds = Path(tfdir).joinpath("credentials.tfrc.json")
        # Ensure the file is created if it doesn't already exist
        self._creds.touch(exist_ok=True)

    def update(self, token: str, url: str):
        """
        This method updates the TF credentials file with the TLM-specific
        credentials generated from the components passed in the invocation.
        """
        tok: Dict[str, str] = {}
        tok["token"] = token
        srv: Dict[str, Any] = {}
        purl = url
        srv[purl] = tok
        creds: Dict[str, Any] = {}
        creds["credentials"] = srv
        with open(self._creds, mode="w", encoding="utf8") as kredz:
            kredz.write(str(TLMJson(struct=creds)))
        print(f"Updated: {self._creds}")
