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

from os.path import relpath
from pathlib import Path
import random

import pytest

from ansys.scade.power_scripts.obfuscator.obfuscator import Obfuscator
from conftest import load_tmp_project_session, seed
from test_utils import cmp_file, get_resources_dir


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
def test_obfuscator_nominal(capsys, base, conf, libraries, internals, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'Obfuscator' / base
    source = base_dir / 'model' / (base + '.etp')
    target_dir = local_tmpdir / 'test_obfuscator_nominal' / base / conf
    project, session = load_tmp_project_session(source, target_dir)
    # make sure the tests provide always the same results
    # seed = reduce(lambda x, y: x + ord(y), base + conf, 0)
    random.setstate(seed)
    # options
    path = Path(project.pathname)
    trace = path.with_name('trace.txt')
    # run the obfuscation
    cls = Obfuscator(str(trace), internals, libraries)
    status = cls.main(session)
    assert status == 0
    # get the reference directory
    ref_dir = base_dir / 'reference' / conf
    # ignore banner if any
    captured = capsys.readouterr()
    # compare all the files present in ref_dir to those in target_dir
    for reference in (ref_dir).glob('**/*'):
        if reference.is_dir():
            continue
        base = relpath(reference, ref_dir)
        target = target_dir / base
        try:
            diff = cmp_file(reference, target, n=0)
        except BaseException as e:
            diff = [str(e)]
        # not captured, thus the loop hereafter
        # stdout.writelines(diff)
        for line in diff:
            print(line, end='')
    captured = capsys.readouterr()
    assert captured.out == ''
