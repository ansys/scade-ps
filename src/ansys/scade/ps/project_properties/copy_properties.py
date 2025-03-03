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

"""Ansys SCADE Power Scripts: Access to SCADE project properties."""

import json
import os
from pathlib import Path
from typing import Dict, List

from scade.model.project.stdproject import Project, get_roots as get_projects

import ansys.scade.apitools.create as create


class CopyProperties:
    """Copy tool properties from a reference projects to other ones."""

    def __init__(self, schema: str):
        # options
        self.schema = Path(schema)

    def main(self, reference: Project, projects: List[Project]) -> int:
        """Entry point for unit testing or reuse."""
        # read the schema
        try:
            schema = json.loads(self.schema.read_text())
        except BaseException as e:
            print(str(e))
            return 1

        # create a dictionaries of properties with the 'relative' attribute
        tool_props = {}
        for tool, props in schema.items():
            for prop in props:
                if prop[0] == '@':
                    prop = prop[1:]
                    relative = True
                else:
                    relative = False
                tool_prop = f'@{tool}:{prop}'
                tool_props[tool_prop] = relative

        # propagate the selected properties from the reference to the other projects
        modified_projects = []
        for project in projects:
            if self.copy_properties(reference, project, tool_props):
                modified_projects.append(project)

        # save modified projects, once everything is done
        for project in modified_projects:
            create.save_project(project)

        return 0

    def copy_properties(self, src: Project, dst: Project, tool_props: Dict[str, bool]) -> bool:
        """Copy the selected properties from src to dst and return whether dst is modified."""
        # return value
        modified = False
        # local caches in the destination project: key = prop.name, configuration.name
        props = {}
        for dst_prop in dst.props:
            if dst_prop.name in tool_props:
                configuration = dst_prop.configuration.name if dst_prop.configuration else ''
                # index the property by its name and configuration
                props[dst_prop.name, configuration] = dst_prop
        configurations = {_.name: _ for _ in dst.configurations}

        # propagate the properties
        for src_prop in src.props:
            prop_name = src_prop.name
            if prop_name not in tool_props:
                continue
            relative = tool_props[prop_name]

            # check the existence of the configuration in the destination project
            if src_prop.configuration:
                conf_name = src_prop.configuration.name
                dst_conf = configurations.get(conf_name)
                if not dst_conf:
                    dst_conf = create.create_configuration(dst, conf_name)
                    configurations[conf_name] = dst_conf
                    modified = True
            else:
                dst_conf = None
                conf_name = ''

            # update the property's values
            values = src_prop.values
            if relative:
                src_dir = Path(src.pathname).parent
                dst_dir = Path(dst.pathname).parent
                new_values = []
                for pathname in values:
                    if pathname and pathname[0] != '$':
                        path = Path(pathname)
                        # make the path absolute wrt the source project
                        path = (src_dir / path).resolve()
                        # make the path relative wrt the destination project
                        path = os.path.relpath(path, start=dst_dir)
                        pathname = str(path)
                    new_values.append(pathname)

                values = new_values

            key = prop_name, conf_name
            dst_prop = props.get(key)
            if not dst_prop:
                # create the property
                print(f'creating {prop_name} for {conf_name}')
                dst_prop = create.create_prop(dst, dst_conf, prop_name, values)
                modified = True
            else:
                if dst_prop.values != values:
                    print(f'updating {prop_name} for {conf_name} with {values}')
                    dst_prop.values = values
                    modified = True
                # remove the property from the cache, remaining ones should be deleted
                props.pop(key)

        # delete unused properties, for example properties having default values
        for dst_prop in props.values():
            dst.props.remove(dst_prop)
            modified = True

        return modified


def main(reference: str, schema: str) -> int:
    """Entry point for ``scade.exe -script`` or called by ``__main__``."""
    ref_project = None
    projects = []
    for project in get_projects():
        if Path(project.pathname).name == reference:
            ref_project = project
        else:
            projects.append(project)
    if not ref_project:  # pragma: nocover
        # this may happen if and only if the script is run with ``scade.exe -script``
        print(f'{reference}: project not found')
        return 1
    code = CopyProperties(schema).main(ref_project, projects)
    return code
