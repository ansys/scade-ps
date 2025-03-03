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

"""Ansys SCADE Power Scripts: Create a template of tool properties schema from a SCADE project."""

import json
from pathlib import Path
import re

from scade.model.project.stdproject import Project, get_roots as get_projects


class CreateTemplate:
    """List the tool properties of a SCADE project."""

    def __init__(self, template_file: str):
        # options
        self.template_file = Path(template_file)

    def dump_template(self, project: Project):
        """Dump the tool properties as a template file for a further copy."""
        # gather all tool properties, per tool
        pattern = re.compile(r'@(\w+):(\w+)')
        tools = {}
        for prop in project.props:
            m = pattern.match(prop.name)
            if m:
                tool, name = m.groups()
                tools.setdefault(tool, set()).add(name)

        # sort the names to ensure some output stability
        sorted_tools = {tool: sorted(names) for tool, names in tools.items()}

        # use json syntax, instead of TCL syntax from legacy tool
        with self.template_file.open('w') as f:
            json.dump(sorted_tools, f, sort_keys=True, indent=4)

    def main(self, project: Project) -> int:
        """Entry point for unit testing or reuse."""
        try:
            self.dump_template(project)
            return 0
        except BaseException as e:
            print(str(e))
            return 1


def main(template_file: str) -> int:
    """Entry point for ``scade.exe -script`` or called by ``__main__``."""
    project = get_projects()[0]
    code = CreateTemplate(template_file).main(project)
    return code
