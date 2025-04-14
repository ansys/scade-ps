New OIDs
########

Description
===========

This sub-command reads the duplicated OIDs from the file produced by the
:doc:`find </user-guide/project-properties/copy>` command, computes new OIDs for each
corresponding element and saves the model.

This command also produces a mapping file (JSON) containing the pairs (old oid, new oid)
as well as the list of the traced requirements, when applicable. This can be used to update
custom references, other than annotations or traceability.

The update of the traceability is performed using the ALM Gateway temporary trace file (ALMGT).
This file is created if it does not exist.

*Reminder, this trace file contains the traceability changes between two ALM Gateway exports.*

The tool inserts commands for removing traceability links for the old OIDs, and commands for adding new
traceability links for new OIDs. It takes into account old OIDs already present in the trace file,
either to add and/or remove a link. A regular ALM Gateway export updates the traceability in the ALM tool.

.. Note::

   The update of the traceability requires Ansys SCADE 2024 R1 or greater.

Usage
=====

.. code:: text

   usage: ansys_scade_ps_change_oids new [-h] -p <project> -f <input file> -m <output map file>

   options:
     -h, --help            show this help message and exit
     -p <project>, --project <project>
                           SCADE Suite project
     -f <input file>, --file <input file>
                           input file
     -m <output map file>, --map <output map file>
                           output map file

For example:

.. code:: bash

   ansys_scade_ps_change_oids new -p P2.etp -f P2.dupoids.txt -m map_oids.json

This command updates the ``P2.etp`` model, as well as the traceability,
and it outputs the mapping between old and new OIDs to ``map_oids.json``,
for example:

.. code:: json

   [
       {
           "new_oid": "!ed/26/5383/4BD0/67c9c6c77d2b",
           "old_oid": "!ed/ab/6461/600C/67c802957b40",
           "path": "MyPackage::",
           "reqs": []
       },
       {
           "new_oid": "!ed/2a/5383/4BD0/67c9c6c75621",
           "old_oid": "!ed/b8/6461/600C/67c802ab52e2",
           "path": "MyPackage::SOME_CONSTANT/",
           "reqs": []
       },
       {
           "new_oid": "!ed/2b/5383/4BD0/67c9c6c71b83",
           "old_oid": "!ed/c1/6461/600C/67c802b54ee5",
           "path": "MyOperator/",
           "reqs": [
               "P3_REQ_001"
           ]
       }
   ]
