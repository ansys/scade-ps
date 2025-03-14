Change OIDs
###########

Rationale
=========

SCADE uses generated unique identifiers (OIDs) to refer internally to model
elements. These OIDs are stored in the project's files.

In some cases, two SCADE projects that have been initiated by copy/paste, then
developed independently, may share many overlapping OIDs. Should these projects
need to be integrated together, this will generate conflicts in the IDE. For
instance, traceability between requirements and model elements, that relies on
OIDs, may be unable to unambiguously resolve.

Description
===========

This tool has several sub-commands described in the following sections.

* ``find``: List the duplicated OIDs
* ``new``: Replace the duplicated OIDs and update references

Usage
=====

.. code:: text

   usage: ansys_scade_ps_change_oids [-h] {find,new} ...

   Ansys SCADE Power Scripts: Change duplicate OIDs

   positional arguments:
     {find,new}       change_oids sub-commands
       find           Find duplicate OIDs
       new            Create new OIDs

   options:
     -h, --help            show this help message and exit

Sub-commands
============

.. toctree::
   :maxdepth: 1

   find
   new
