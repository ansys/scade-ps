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
Test suite for default_notes.py.

Test strategy:

The tests of this module make a copy of a reference project, create default notes
and add compare the result files to a reference.
"""

from os.path import relpath

import pytest

from ansys.scade.ps.default_notes.default_notes import DefaultNotes
from conftest import load_tmp_project_session
from test_utils import cmp_file, get_resources_dir


@pytest.mark.parametrize('base', ['Nominal'])
def test_default_notes_nominal(capsys, base, local_tmpdir):
    base_dir = get_resources_dir() / 'resources' / 'DefaultNotes' / base
    source = base_dir / 'model' / (base + '.etp')
    target_dir = local_tmpdir / 'test_default_notes_nominal' / base
    project, session = load_tmp_project_session(source, target_dir)
    # create default notes
    cls = DefaultNotes()
    status = cls.main(session)
    assert status == 0
    # get the reference directory
    ref_dir = base_dir / 'reference'
    # reset captured output
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


def test_default_notes_empty(capsys, local_tmpdir):
    """Empty is a model with no annotation schema."""
    base = 'Empty'
    base_dir = get_resources_dir() / 'resources' / 'DefaultNotes' / base
    source = base_dir / 'model' / (base + '.etp')
    target_dir = local_tmpdir / 'test_default_notes_empty' / base
    project, session = load_tmp_project_session(source, target_dir)
    # reset captured output
    captured = capsys.readouterr()
    # create default notes
    cls = DefaultNotes()
    status = cls.main(session)
    assert status == 0
    # nothing should have been reported
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    # neither created
    ann_files = [_ for _ in (target_dir).glob('**/*.ann')]
    assert not ann_files
