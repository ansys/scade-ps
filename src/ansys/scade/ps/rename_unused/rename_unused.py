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

"""Ansys SCADE Power Scripts: Rename unused files."""

from pathlib import Path

from scade.model.project.stdproject import Project, get_roots as get_projects

tool = 'Ansys SCADE Power Scripts: Rename unused files'


class RenameUnused:
    """Renames unused files (SCADE, XSCADE, ANN)."""

    def main(self, project: Project) -> int:
        """Entry point for unit testing or reuse."""
        # cache files
        file_refs = [Path(_.pathname) for _ in project.file_refs]
        scade_files = {_ for _ in file_refs if _.suffix.lower() in ['.scade', '.xscade']}
        dir = Path(project.pathname).parent
        # model files
        for pattern in ['*.scade', '*.xscade']:
            for file in dir.glob(pattern):
                if file not in scade_files:
                    self.rename(file)
        # annotation files
        for file in dir.glob('*.ann'):
            # check xscade files only: scade files do not have annotations
            model_file = file.with_suffix('.xscade')
            if model_file not in scade_files:
                self.rename(file)
        return 0

    def rename(self, file: Path):
        """Suffix the file name with ``.toremove``."""
        print(f'renaming {file.name}')
        file.rename(file.with_name(file.name + '.toremove)'))


def main() -> int:
    """Entry point for ``scade.exe -script`` or called by ``__main__``."""
    return_code = 0
    for project in get_projects():
        code = RenameUnused().main(project)
        if code != 0:
            return_code = code

    return return_code
