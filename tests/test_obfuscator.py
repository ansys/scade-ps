# -*- coding: utf-8 -*-

# Copyright (C) 2025 ANSYS, Inc. and/or its affiliates.
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

"""
Test suite for obfuscator.py.

Test strategy:

The tests of this module make a copy of a reference project, obfuscate it and add
compare the result files to a reference.
"""

from pathlib import Path
import subprocess
import sys
from typing import List

import pytest

from conftest import load_tmp_project
from test_utils import diff_directories, get_resources_dir


def _run_obfuscator(exe: bool, args: List[str], expected: int, ref: Path, dst: Path):
    """
    Run obfuscator with the specified command-line parameters.

    The test is successful if:

    * the return code is the expected one
    * the produced files are identical to the reference ones
    """
    if exe:
        cmd = [
            str(Path(sys.executable).with_name('ansys_scade_ps_obfuscator.exe')),
        ]
    else:
        cmd = [
            sys.executable,
            '-m',
            'ansys.scade.ps.obfuscator',
        ]
    cmd.extend(args)
    status = subprocess.run(cmd, capture_output=True)
    if status.stderr:
        print(status.stderr.decode('utf-8').strip('\n'))
    if status.stdout:
        print(status.stdout.decode('utf-8').strip('\n'))
    assert status.returncode == expected
    if expected == 0:
        # no error, compare files
        failure = diff_directories(ref, dst)
        assert not failure


def format_test_data(data: list) -> list:
    """Set the test id to the name of the fields project and conf."""
    return [pytest.param(*_, id=('-'.join(_[0:2])) if _[1] else _[0]) for _ in data]


@pytest.mark.parametrize(
    'base, conf, libraries, internals',
    format_test_data(
        [
            ('Nominal', 'Default', [], False),
            ('Nominal', 'Internals', [], True),
            ('Libraries', 'None', ['First', 'Second'], False),
            ('Libraries', 'NoFirst', ['First'], False),
            ('Libraries', 'NoSecond', ['Second'], False),
            ('Libraries', 'All', [], False),
        ]
    ),
)
def test_obfuscator_nominal(base, conf, libraries, internals, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'Obfuscator' / base
    source = base_dir / 'model' / (base + '.etp')
    target_dir = local_tmpdir / 'test_obfuscator_nominal' / base / conf
    project = load_tmp_project(source, target_dir)
    # options
    path = Path(project.pathname)
    trace = path.with_name('trace.txt')
    # get the reference directory
    ref_dir = base_dir / 'reference' / conf
    # run the obfuscation
    args = ['-p', project.pathname, '-s', 'obfuscator']
    if trace:
        args.extend(['-t', str(trace)])
    if internals:
        args.append('-i')
    if libraries:
        args.extend(['-l'] + libraries)
    # reuse the boolean internals to select the launch mode
    exe = internals
    _run_obfuscator(exe, args, 0, ref_dir, target_dir)
