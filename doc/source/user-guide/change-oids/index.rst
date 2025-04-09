Change OIDs
###########

Rationale
=========

SCADE uses generated unique identifiers (OIDs) to refer internally to model
elements. These OIDs are stored in the model's files.

A SCADE project that has been initiated by copying files from an existing one
contains many duplicated OIDs. Should these projects need to be integrated
together, conflicts would happen in the integration with external tools that
rely on OIDs to refer to model elements. For instance, traceability between
requirements in an external ALM tool and model elements would be unable
to unambiguously resolve.

.. Note::

   When initiating a project from another one, a best practice is to copy/paste
   packages and other model elements directly from the SCADE IDE rather than from
   the file system.

.. Note::

   **This tool requires Ansys SCADE 2024 R1 or greater.**

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
