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

"""Ansys SCADE Power Scripts: Update traceability with respect to new OIDs."""

from pathlib import Path
from typing import Dict, List

from lxml import etree as et


class LLR:
    """Entry of a trace file (ALMGT)."""

    def __init__(self, id: str = '', path: str = ''):
        self.elem = None
        self.id = id
        self.path = path
        self.adds = {}
        self.rems = {}

    def is_empty(self):
        """Return whether the LLR has links to add or remove."""
        return len(self.adds) + len(self.rems) == 0

    def parse(self, elem):
        """Parse the XML element's hierarchy."""
        self.elem = elem
        self.id = self.elem.get('id')
        self.path = self.elem.get('pathName', '')
        for elem in self.elem.findall('requirement'):
            req = elem.get('id')
            kind = elem.get('traceType')
            if kind == 'ADD_LINK':
                self.adds[req] = elem
            else:
                self.rems[req] = elem
        return self

    def update_tree(self):
        """Create the missing xml elements."""
        for req, elem in self.adds.items():
            if elem is None:
                et.SubElement(self.elem, 'requirement', {'id': req, 'traceType': 'ADD_LINK'}, None)

        for req, elem in self.rems.items():
            if elem is None:
                et.SubElement(
                    self.elem, 'requirement', {'id': req, 'traceType': 'REMOVE_LINK'}, None
                )

    def remove(self, req: str) -> bool:
        """Remove a link to a requirement."""
        if req in self.rems:
            # requirement being removed: nothing to do
            return False
        elif req in self.adds:
            # new requirement: remove it from the list
            elem = self.adds.pop(req)
            assert self.elem is not None  # nosec B101  # addresses linter
            self.elem.remove(elem)
        else:
            # register for deletion
            self.rems[req] = None
        return True

    def add(self, req: str):
        """Add a link to a requirement."""
        self.adds[req] = None


class GTFile:
    """Content of SCADE ALM Gateway traceability cache file(ALMGT)."""

    def __init__(self):
        self.tree = None
        self.llrs = {}

    def parse(self, trace: Path) -> bool:
        """Parse the trace file."""
        parser = et.XMLParser(remove_blank_text=True)
        try:
            self.tree = et.parse(str(trace), parser)
        except OSError as e:
            print(e)
            return False
        for elem in self.tree.getroot().findall('object'):
            llr = LLR().parse(elem)
            self.llrs[llr.id] = llr
        return True

    def save(self, trace: Path):
        """Save the trace file."""
        assert self.tree is not None  # nosec B101  # addresses linter
        root = self.tree.getroot()
        for llr in self.llrs.values():
            if llr.is_empty():
                if llr.elem is not None:
                    root.remove(llr.elem)
                continue
            if llr.elem is None:
                # sounds like path is no more present in traceability files (ALMGT)
                # llr.elem = et.SubElement(root, 'object', {'id': llr.id, 'path': llr.path}, None)
                llr.elem = et.SubElement(root, 'object', {'id': llr.id}, None)
            llr.update_tree()
        self.tree.write(
            str(trace), encoding='utf-8', standalone='yes', xml_declaration=True, pretty_print=True
        )

    def replace_oid(self, subst: Dict[str, str]):
        """Add an entry to replace an oid if the element traces requirements."""
        reqs = subst['reqs']
        if not reqs:
            return
        path = subst['path']
        old_oid = subst['old_oid']
        new_oid = subst['new_oid']
        old_llr = self.llrs.setdefault(old_oid, LLR(old_oid, path))
        new_llr = LLR(new_oid, path)
        self.llrs[new_oid] = new_llr
        for req in reqs:
            if old_llr.remove(req):
                new_llr.add(req)


def update_trace(substs: List[Dict[str, str]], trace: Path) -> bool:
    """Update trace file (ALMGT) with the changes recorded in map_oids."""
    if not trace.exists():
        # load the almgt template file, same directory as the script
        source = Path(__file__).parent / 'template.almgt'
    else:
        source = trace
    gt = GTFile()
    if gt.parse(source):
        for subst in substs:
            gt.replace_oid(subst)
        gt.save(trace)
        return True
    return False
