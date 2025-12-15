# -*- coding: utf-8 -*-
# Copyright TLM Partners, Inc. All Rights Reserved
""" PLACEHOLDER """
import shutil
from pathlib import Path
from typing import List
from tlmcore.shellcmd import TLMShellCmd

PYHDR = "# -*- coding: utf-8 -*-\n# Copyright TLM Partners, Inc. All Rights Reserved"


class PypiVersion:
    """PLACEHOLDER"""

    SUPPORTED_LEVELS = ["patch", "minor", "major"]

    def __init__(self, name: str, level: str = "patch") -> None:
        """PLACEHOLDER"""
        # Reminder: refactor this
        # pylint: disable=duplicate-code
        self.version_str = "0.0.0"
        self.new_version_str = "0.0.0"
        if level not in self.SUPPORTED_LEVELS:
            raise ValueError(
                f"Unsupported patch level: {level} - use one of {self.SUPPORTED_LEVELS}"
            )
        self.patch_level = level
        self.modname = name
        self.major = 0
        self.minor = 0
        self.patch = 0
        self._check_package_version()
        self._uptick()

    def _version_extractors(self, pstr: str) -> None:
        substr1: List[str] = pstr.split("(")
        substr2: List[str] = substr1[1].split(")")
        self.version_str = substr2[0]
        substr3: List[str] = self.version_str.split(".")
        self.major = int(substr3[0])
        self.minor = int(substr3[1])
        self.patch = int(substr3[2])

    def _check_package_version(self) -> None:
        comm: List[str] = ["python3", "-m", "pip", "index", "versions"]
        comm.append(self.modname)
        result: TLMShellCmd = TLMShellCmd(cspec=comm, capture=True)
        if result.errors:
            return
        for res in result.output:
            if res.startswith("ERROR:"):
                break
            if res.startswith(self.modname):
                self._version_extractors(pstr=res)

    def _uptick(self) -> None:
        # Reminder: refactor this
        # pylint: disable=duplicate-code
        if self.patch_level == "patch":
            self.patch += 1
        if self.patch_level == "minor":
            self.patch = 0
            self.minor += 1
        if self.patch_level == "major":
            self.patch = 0
            self.minor = 0
            self.major += 1
        self.new_version_str = f"{self.major}.{self.minor}.{self.patch}"

    @property
    def version(self) -> str:
        """Accessor"""
        return self.version_str

    @property
    def new_version(self) -> str:
        """Accessor"""
        return self.new_version_str


class PythonPackage:
    """PLACEHOLDER"""

    PYPROJECT_TOML = """[build-system]
requires = [
    \"setuptools>=42\",
    \"wheel\"
]
build-backend = \"setuptools.build_meta\"
"""

    PYTEST_INI = """[pytest]
addopts = -s
pythonpath = 
    src
"""

    TEST_DUMMY = """from __future__ import print_function
import pytest


class Test_Dummy(object):
    def test_add(self):
        assert True
"""

    SETUP_CFG = """[metadata]
name = {NAME}
version = 0.0.1
author = Fill Me In
author_email = fill.me.in@tlmpartners.com
description = TLM Python undescribed package
long_description = file: README.md
long_description_content_type = text/markdown
classifiers =
    Programming Language :: Python :: 3
    License :: Proprietory
    Operating System :: OS Independent

[options]
package_dir =
    = .
packages = find:
python_requires = >=3.

[options.packages.find]
where = .
"""

    MAKE_PROLOG = """# Copyright TLM Partners, Inc. All Rights Reserved
#
MODULE := {NAME}
#

"""

    MAKE_EPILOG = """# OPTIONAL
# If your package has dependencies on other TLM packages in this tree,
# defining those dependencies here will help ensure overall code quality.
# PYLINT_DEPS := ../<name1>/src ../<name2>/src 
#
UPVERSION := $(shell igor py vnum-plus ${MODULE})
# Pylint can exploit available cores to accelerate static checking
PARALLEL = $(shell nproc)

# The test target will execute unit tests
.PHONY: test
test:
	python3 -m pytest

# The lint target executes static checking with pylint
.PHONY: lint
lint:
	python3 -m pylint -j ${PARALLEL} src/ ${PYLINT_DEPS}

# The typehint target uses mypy to check the consistency of typehint usage across the source
# The use of type hints is encouraged to improve/maintain code quality
.PHONY: typehint
typehint:
	python3 -m mypy --ignore-missing-imports --check-untyped-defs src/

# The format target ensures that all source code is formatted consistently
# and conforms to a uniform coding style.
.PHONY: format
format:
	python3 -m black src/*/*.py

# The check target ensures that all formatting, quality checks and unit tests are completed.
.PHONY: check
check: format lint typehint test

# The clean target removes leftover cruft
.PHONY: clean
clean:
	rm -fr dist .mypy_cache .pytest_cache

# The deploy target will run all checks and attempt to deploy a clean package update if it passes.
.PHONY: deploy
deploy: check clean
	tbump --non-interactive --only-patch ${UPVERSION}
	python3 -m build --no-isolation
	python3 -m twine upload -r local dist/* --verbose
	rm -fr dist

"""

    TOML_EPILOG = """[[file]]
src = "src/{NAME}/__init__.py"
search = '__version__ = "{CURRENT_VERS}"'
"""

    def __init__(self, name: str) -> None:
        """PLACEHOLDER"""
        self._name: str = name
        self._pwd: Path = Path.cwd()
        self._py: Path = Path(self._pwd, "py")
        self._module: Path = Path(self._py, self._name)
        self._src: Path = Path(self._module, "src", self._name)
        self._tests: Path = Path(self._module, "tests")
        self.process()

    def _create_init_py(self) -> None:
        """Create an empty module __init__.py in the module source code directory."""
        init_py: Path = Path(self._src, "__init__.py")
        # Don't overwrite if module already populated
        if init_py.exists():
            return
        dmdocstr = '""" Module Doc String """'
        vrs = '"0.0.1"'
        boilerplate = f"{PYHDR}\n{dmdocstr}\n__version__ = {vrs}"
        with init_py.open(mode="w", encoding="utf-8") as inpy:
            inpy.write(boilerplate)

    def _create_pyproject_toml(self) -> None:
        """Create the pyproject.toml file in the module top directory"""
        pyp_toml: Path = Path(self._module, "pyproject.toml")
        # Don't overwrite if config already populated
        if pyp_toml.exists():
            return
        with pyp_toml.open(mode="w", encoding="utf-8") as pyprj:
            pyprj.write(self.PYPROJECT_TOML)

    def _create_pytest_ini(self) -> None:
        """Create the pytest.ini file in the module top directory"""
        pytst_ini: Path = Path(self._module, "pytest.ini")
        # Don't overwrite if config already populated
        if pytst_ini.exists():
            return
        with pytst_ini.open(mode="w", encoding="utf-8") as pytst:
            pytst.write(self.PYTEST_INI)

    def _create_test(self) -> None:
        """Create the dummy test case file in the module tests subdirectory"""
        test: Path = Path(self._tests, "test_dummy.py")
        # Don't overwrite if test already populated
        if test.exists():
            return
        with test.open(mode="w", encoding="utf-8") as tst:
            tst.write(self.TEST_DUMMY)

    def _create_setup_cfg(self) -> None:
        setup_cfg: Path = Path(self._module, "setup.cfg")
        # Don't overwrite if setup.cfg already populated
        if setup_cfg.exists():
            return
        with setup_cfg.open(mode="w", encoding="utf-8") as stp:
            stp.write(self.SETUP_CFG.format(NAME=self._name))

    def _create_tbump_toml(self) -> None:
        tbump_toml: Path = Path(self._module, "tbump.toml")
        # Don't overwrite if tbump.toml already populated
        if tbump_toml.exists():
            return
        tbump_tmpl: Path = Path(self._py, "template4tbump.toml")
        if tbump_tmpl.exists():
            shutil.copy(tbump_tmpl, tbump_toml)
        versioning = self.TOML_EPILOG.format(
            NAME=self._name, CURRENT_VERS=r"{current_version}"
        )
        with tbump_toml.open(mode="a", encoding="utf8") as tbump:
            tbump.write(versioning)

    def _create_makefile(self) -> None:
        makefile: Path = Path(self._module, "Makefile")
        # Don't overwrite if Makefile already populated
        if makefile.exists():
            return
        mk_prolog: str = self.MAKE_PROLOG.format(NAME=self._name)
        make_fyle: str = f"{mk_prolog}{self.MAKE_EPILOG}"
        with makefile.open(mode="w", encoding="utf-8") as mkf:
            mkf.write(make_fyle)

    def process(self) -> None:
        """PLACEHOLDER"""
        # Create the module directory subtree
        self._src.mkdir(parents=True, exist_ok=True)
        self._tests.mkdir(parents=True, exist_ok=True)
        # Create a placeholder with a dummy test case
        self._create_test()
        # Module config files
        self._create_init_py()
        self._create_pyproject_toml()
        self._create_pytest_ini()
        self._create_setup_cfg()
        self._create_tbump_toml()
        self._create_makefile()

    @property
    def name(self) -> str:
        """Accessor"""
        return self._name

    @property
    def src_path(self) -> str:
        """Accessor"""
        return str(self._src.absolute())

    @property
    def module_path(self) -> str:
        """Accessor"""
        return str(self._module.absolute())
