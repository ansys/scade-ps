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

"""Ansys SCADE Power Scripts: Change duplicate OIDs."""

import json
from pathlib import Path

import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit

try:
    import scade.model.traceability as traceability
except ModuleNotFoundError:
    # module exists only since SCADE 2024 R1
    traceability = None

from ansys.scade.ps.change_oids.update_trace import update_trace


class _Logger:
    """Logging support."""

    def __init__(self, file: str):
        self.f = Path(file).open('w') if file else None

    def log(self, *args):
        """Log a message either to a file or the standard output."""
        if self.f:
            self.f.write(' '.join(args) + '\n')
        else:
            print(*args)


class NewOids(Visit):
    """Ansys SCADE Power Scripts: Change duplicate OIDs."""

    def __init__(self, file: str, map: str, log: str):
        self.file = Path(file)
        self.map = Path(map)
        self.log = _Logger(log)
        # cache
        self.map_oids = {}  # Dict[str, suite.Annotable]
        # substitutions done
        self.substs = []  # List[Dict[str, str]]
        # requirements
        self.map_traceability_links = {}  # Dict[str, List[str]]

    def main(self, session: suite.Session) -> int:
        """Entry point for unit testing or reuse."""
        # index the model elements by oid
        self.visit(session.model)
        # read the duplicated oids: ignore comments and optional paths
        oids = [_.split('\t')[0] for _ in self.file.read_text().split('\n') if _ and _[0] != '#']

        # read the requirements, if any
        path = Path(session.model.project.pathname)
        if traceability:
            try:
                req_project = traceability.load(str(path))
            except BaseException:
                req_project = None
        else:
            req_project = None
        if req_project:
            for element in req_project.traceable_elements:
                self.map_traceability_links[element.identifier] = [
                    _.target.identifier for _ in element.outgoing_links
                ]
        else:
            self.map_traceability_links = {}
        # compute new oids
        for oid in oids:
            annotable = self.map_oids.get(oid)
            if not annotable:
                self.log.log(f'{oid}: model element not found')
            else:
                if not self.process_element(annotable):
                    # no need to continue
                    return 1

        # update the traceability links (ALMGT)
        trace = Path(session.model.project.pathname).with_suffix('.almgt')
        if not update_trace(self.substs, trace):
            return 1

        # dump the mapping
        try:
            with self.map.open('w') as f:
                json.dump(self.substs, f, indent=4, sort_keys=True)
        except BaseException as e:
            self.log.log(str(e))
            return 1

        # save modified model and annotation files
        session.save_model2()

        return 0

    def process_element(self, annotable: suite.Annotable) -> bool:
        """Change the oid of a model element and record updates."""
        self.log.log(f'updating oid for {self.get_path(annotable)}')
        old_oid = annotable.get_oid()
        # create a new oid using a ghost object, for example a constant
        new_oid = suite.Constant().get_oid()
        # requirement_ids not available for scripts executed outside of the SCADE IDE
        # reqs = annotable.requirement_ids if isinstance(annotable, suite.Traceable) else []
        reqs = self.map_traceability_links.get(annotable.get_oid(), [])
        self.substs.append(
            {
                'path': self.get_path(annotable),
                'old_oid': old_oid,
                'new_oid': new_oid,
                'reqs': reqs,
            }
        )

        try:
            # available only in recent releases of SCADE Suite (starting 2021 R2?)
            annotable.set_oid(new_oid)
        except BaseException as e:
            self.log.log(str(e))
            return False
        unit = annotable.defined_in
        unit.sao_modified = True
        if isinstance(annotable, suite.Annotable) and annotable.ann_notes:
            unit.ann_modified = True

        return True

    def get_path(self, object_: suite.Object) -> str:
        """
        Provide a Scade path for objects that don't have one.

        For objects that don't have a path, the function returns their name
        appended to their owner's path. Otherwise, returns their own path.
        """
        if isinstance(object_, suite.TreeDiagram):
            path = object_.owner.get_full_path() + f'<{object_.block_kind}>'
        elif isinstance(object_, suite.CompositeElement):
            return object_.owner.get_full_path() + f'<{object_.name}>'
        else:
            path = object_.get_full_path()

        return path

    def visit_annotable(self, annotable: suite.Annotable, *args):
        """Index the model element by oid."""
        self.map_oids[annotable.get_oid()] = annotable
        super().visit_annotable(annotable, *args)


def main(file: str, map: str, log: str = '') -> int:
    """Entry point for ``scade.exe -script`` or called by ``__main__``."""
    code = NewOids(file, map, log).main(get_sessions()[0])
    return code
