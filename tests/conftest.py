# -*- coding: utf-8 -*-

# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Unit tests fixtures."""

import difflib
from os.path import relpath
from pathlib import Path
import random
from shutil import copytree, rmtree
import subprocess
import sys
from typing import List, Optional

import pytest

import ansys.scade.apitools  # noqa: F401

# must be imported after scade_env
# isort: split
import scade
import scade.model.project.stdproject as std
import scade.model.suite as suite

from ansys.scade.apitools.info import get_scade_version

# initialize the seed and store the state to get reproducible tests
random.seed('obfuscator')
seed = random.getstate()


def pytest_configure(config):
    """Declare the markers used in this project."""
    config.addinivalue_line('markers', 'project: project to be loaded')


def get_resources_dir() -> Path:
    """Return the directory ./resources relative to this file's directory."""
    script_path = Path(__file__).resolve()
    return script_path.parent


@pytest.fixture(scope='session')
def local_tmpdir():
    """Create/empty the temporary directory for output files."""
    path = Path('tests') / 'tmp'
    try:
        rmtree(str(path))
    except FileNotFoundError:
        pass
    path.mkdir()
    return path


def load_session(pathname: Path) -> suite.Session:
    """
    Load a Scade model in a separate environment.

    Note: The model can have unresolved references since the libraries
    are not loaded.
    """
    session = suite.Session()
    session.load2(str(pathname))
    assert session.model
    return session


def load_project(pathname: Path) -> std.Project:
    """
    Load a Scade project in a separate environment.

    Note: Undocumented API.
    """
    # scade is a CPython module defined dynamically
    project = scade.load_project(str(pathname))  # type: ignore
    return project


def load_tmp_project(path: Path, target_dir: Path) -> std.Project:
    """Load a temporary copy of the project."""
    # duplicate the project to edit it safely
    copytree(path.parent, target_dir)
    path = target_dir / path.name
    project = load_project(path)
    return project


def cmp_file(fromfile: Path, tofile: Path, n=3, linejunk=None):
    """Return the differences between two files."""
    with fromfile.open() as fromf, tofile.open() as tof:
        if linejunk:
            fromlines = [line for line in fromf if not linejunk(line)]
            tolines = [line for line in tof if not linejunk(line)]
        else:
            fromlines, tolines = list(fromf), list(tof)

    diff = difflib.context_diff(fromlines, tolines, str(fromfile), str(tofile), n=n)
    return diff


def diff_files(ref: Path, dst: Path) -> bool:
    print('compare', str(ref), str(dst))
    diffs = cmp_file(ref, dst)
    failure = False
    for d in diffs:
        print(d.rstrip('\r\n'))
        failure = True
    return failure


def diff_directories(ref_dir: Path, dst_dir: Path) -> bool:
    failure = False
    for reference in (ref_dir).glob('**/*'):
        if reference.is_dir():
            continue
        base = relpath(reference, ref_dir)
        target = dst_dir / base
        print('compare', str(reference), str(target))
        try:
            diff = cmp_file(reference, target, n=0)
        except BaseException as e:
            diff = [str(e)]
        # not captured, thus the loop hereafter
        # stdout.writelines(diff)
        for line in diff:
            print(line, end='')
            failure = True
    return failure


def run_tool(
    module: str, args: List[str], ref: Optional[Path] = None, dst: Optional[Path] = None
) -> subprocess.CompletedProcess:
    """
    Run a tool with the specified command-line parameters.

    The test is successful if:

    * the return code is the expected one
    * the produced files are identical to the reference ones
    """
    if module.endswith('.exe'):
        cmd = [str(Path(sys.executable).with_name(module))]
    else:
        cmd = [sys.executable, '-m', module]
    cmd.extend([str(_) for _ in args])
    status = subprocess.run(cmd, capture_output=True)
    if status.stderr:
        for line in status.stderr.splitlines():
            print(line.decode('utf-8'))
    if status.stdout:
        for line in status.stdout.splitlines():
            print(line.decode('utf-8'))
    if status.returncode == 0 and ref:
        # no error, compare files
        assert dst
        if ref.is_dir():
            failure = diff_directories(ref, dst)
        else:
            failure = diff_files(ref, dst)
        assert not failure
    return status


def filter_stderr(stderr: str) -> str:
    """Filter coverage warnings from ``pytest-cov``."""
    if get_scade_version() <= 231:
        text = '\n'.join(
            [
                _
                for _ in stderr.split('\n')
                if 'CoverageWarning' not in _ and 'real_section, unknown, filename' not in _
            ]
        )
    else:
        text = stderr
    return text
