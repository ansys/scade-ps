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

"""Script example for setting hard-coded properties values in a project."""

from pathlib import Path

from scade.model.project.stdproject import get_roots as get_projects

from ansys.scade.apitools.create import create_configuration, save_project

for project in get_projects():
    configuration = project.find_configuration('KCG')
    # make sure the configuration exists
    if not configuration:
        configuration = create_configuration(project, 'KCG')

    # set a scalar property based on the project's name
    base_name = Path(project.pathname).stem
    DEFAULT_TARGET_DIR = ''  # this is not the exact default value, it does not matter here
    project.set_scalar_tool_prop_def(
        'GENERATOR',
        'TARGET_DIR',
        f'../code/{base_name}',
        DEFAULT_TARGET_DIR,
        configuration,
    )

    # set a boolean property
    DEFAULT_DEBUG = False
    project.set_bool_tool_prop_def('GENERATOR', 'DEBUG', False, DEFAULT_DEBUG, configuration)

    # set a regular property: list of values
    extensions = ['SdyChecker', 'SnapshotApi']
    project.set_tool_prop_def('GENERATOR', 'OTHER_EXTENSIONS', extensions, [], configuration)

    # save the project
    save_project(project)
