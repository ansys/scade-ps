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

"""Ansys SCADE Power Scripts: Change duplicate OIDs."""

from pathlib import Path
from typing import List, Set

import scade.model.suite as suite
from scade.model.suite import get_roots as get_sessions
from scade.model.suite.visitors import Visit


class CacheOids(Visit):
    """Visitor to cache the duplicated OIDs."""

    def __init__(self, oids: Set[str], model: suite.Model):
        # global set of oids
        self.oids = oids
        self.model = model
        # duplicated oids
        self.duplicates = []  # type: List[suite.Annotable]
        # run the visit, model only: no libraries
        self.visit(model)

    def visit_annotable(self, annotable: suite.Annotable, *args):
        """Cache the object's oid and check whether it already exists."""
        oid = annotable.get_oid()
        if oid:
            # ignore instances without oid, like array or structures
            if oid in self.oids:
                self.duplicates.append(annotable)
            else:
                self.oids.add(oid)
        super().visit_annotable(annotable, *args)


class FindDuplicates:
    """Find duplicate OIDs for a set of SCADE Suite models."""

    def __init__(self, extension: str, dump_paths: bool):
        # options
        self.extension = extension
        self.dump_paths = dump_paths

    def main(self, sessions: List[suite.Session]) -> int:
        """Entry point for unit testing or reuse."""
        code = 0
        # global set of oids
        oids = set()
        # find duplicate oids
        caches = [CacheOids(oids, session.model) for session in sessions]
        # duymp the results
        for cache in caches:
            path = Path(cache.model.project.pathname).with_suffix(self.extension)
            try:
                f = path.open('w')
            except Exception as e:
                print(str(e))
                # an error occurred
                code = 1
                continue
            # actually, oid is useless
            for item in cache.duplicates:
                tokens = [item.get_oid()]
                if self.dump_paths:
                    tokens.append(self.get_path(item))
                f.write('%s\n' % '\t'.join(tokens))
            f.close()

        return code

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


def main(extension: str, use_paths: bool) -> int:
    """Entry point for ``scade.exe -script`` or called by ``__main__``."""
    code = FindDuplicates(extension, use_paths).main(get_sessions())
    return code
