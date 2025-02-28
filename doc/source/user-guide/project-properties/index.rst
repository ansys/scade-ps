Project properties
##################

Description
===========

This tool has several sub-commands described in the following sections.

Usage
=====

.. code:: bash

   usage: ansys_scade_ps_project_properties [-h] -p <project> {template,} ...

   Ansys SCADE Power Scripts: Access to SCADE project properties

   positional arguments:
     {template}       project properties sub-commands
       template            Create a schema template

   options:
     -h, --help            show this help message and exit
     -p <project>, --project <project>
                           SCADE Suite project

Sub-commands
============

.. toctree::
   :maxdepth: 1

   template
