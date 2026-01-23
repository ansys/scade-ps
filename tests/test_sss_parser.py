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

"""Unit tests for scenario parser."""

from pathlib import Path

from ansys.scade.ps.optimize_sss.scenparser import SSSParser
from conftest import cmp_file


class TestSssParser(SSSParser):
    def on_cycle(self, count: str):
        print('c', count)

    def on_set(self, path: str, value: str):
        print('p', path, 'v', value)

    def on_check(self, path: str, value: str, sustain: str, real: str):
        print('p', path, 'v', value, 's', sustain, 'r', real)

    def on_uncheck(self, path: str):
        print('p', path)

    def on_set_tolerance(self, path: str, real: str):
        print('p', path, 'r', real)

    def on_alias(self, alias: str, path: str):
        print('a', alias, 'p', path)

    def on_comment(self, line: str):
        print(line)


def test_sss_parser_re(capsys, tmpdir):
    test_dir = Path(__file__).parent
    # ignore any message issued prior this text: banner, etc.
    captured = capsys.readouterr()
    TestSssParser().load(test_dir / 'resources' / 'OptimizeSss' / 'parser.sss')
    captured = capsys.readouterr()
    ref = test_dir / 'ref' / 'OptimizeSss' / 'test_sss_parser_re.txt'
    output = Path(tmpdir) / 'test_sss_parser_re.txt'
    with output.open('w') as f:
        f.write(captured.out)
    diff = cmp_file(ref, output, n=0)
    for line in list(diff):
        print(line, end='')
    # stdout.writelines(diff)
    captured = capsys.readouterr()
    assert captured.out == ''
