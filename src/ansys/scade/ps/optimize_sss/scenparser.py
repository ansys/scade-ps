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

"""Parser for SCADE Test scenarios."""

from abc import ABC, abstractmethod
from pathlib import Path
from re import compile


class SSSParser(ABC):
    """Parser abstraction for SCADE Test scenarios."""

    def __init__(self):
        self.re_cycle = compile(r'^SSM::cycle(?:\s+(\d+))?$')
        self.re_set = compile(r'^SSM::set\s+([^\s]+)\s+(.*)$')
        self.re_check = compile(
            r'^SSM::check\s+([^\s]+)\s+(.*?)(?:\s+sustain=(\w+))?(?:\s+real=(.*))?$'
        )
        self.re_uncheck = compile(r'^SSM::uncheck\s+(.*)$')
        self.re_set_tolerance = compile(r'^SSM::set_tolerance(?:\s+path=([^\s]+))?\s+real=(.*)$')
        self.re_alias = compile(r'^SSM::alias\s+(\w+)\s+(.*)$')

    # -----------------------------------------------------------------------
    # semantic actions
    # -----------------------------------------------------------------------

    @abstractmethod
    def on_cycle(self, count: str):
        """Perform semantic action for ``SSM::cycle`` directive."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def on_set(self, path: str, value: str):
        """Perform semantic action for ``SSM::set`` directive."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def on_check(self, path: str, value: str, sustain: str, real: str):
        """Perform semantic action for ``SSM::check`` directive."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def on_uncheck(self, path: str):
        """Perform semantic action for ``SSM::uncheck`` directive."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def on_set_tolerance(self, path: str, real: str):
        """Perform semantic action for ``SSM::set_tolerance`` directive."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def on_alias(self, alias: str, path: str):
        """Perform semantic action for ``SSM::alias`` directive."""
        raise NotImplementedError('Abstract method call')

    @abstractmethod
    def on_comment(self, line: str):
        """Register comments."""
        raise NotImplementedError('Abstract method call')

    # -----------------------------------------------------------------------
    # parsing
    # -----------------------------------------------------------------------

    def load(self, pathname: Path) -> bool:
        """Parse a SCADE Test scenario and return whether it is successful."""
        actions = {
            (self.re_set, self.on_set),
            (self.re_check, self.on_check),
            (self.re_cycle, self.on_cycle),
            (self.re_alias, self.on_alias),
            (self.re_set_tolerance, self.on_set_tolerance),
            (self.re_uncheck, self.on_uncheck),
        }

        try:
            f = pathname.open()
        except OSError as e:
            print(str(e))
            return False

        for line in f:
            line = line.strip('\n').strip()
            if len(line) == 0:
                continue

            if line[0] == '#':
                self.on_comment(line)
                continue

            for r, callback in actions:
                m = r.match(line)
                if m:
                    callback(*m.groups())
                    break
            else:
                print('syntax error:', line)
                return False

        return True
