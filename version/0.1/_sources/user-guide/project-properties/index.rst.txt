Project properties
##################

Rationale
=========

Some software projects may be composed of dozens of interconnected SCADE models.
Maintaining a consistent set of settings across all projects is important, to
ensure homogeneous code generation parameters or modeling rules. However,
performing this maintenance by hand can be cumbersome and error-prone.

Description
===========

This tool has several sub-commands described in the following sections.

- ``template``: initiate, from a reference SCADE project, a list of properties
  and their default values
- ``copy``: propagate default properties to another SCADE project

Usage
=====

.. code:: text

   usage: ansys_scade_ps_project_properties [-h] -p <project> {template,copy} ...

   Ansys SCADE Power Scripts: Access to SCADE project properties

   positional arguments:
     {template,copy}       project properties sub-commands
       template            Create a schema template
       copy                Copy tool properties

   options:
     -h, --help            show this help message and exit
     -p <project>, --project <project>
                           SCADE Suite project

Sub-commands
============

.. toctree::
   :maxdepth: 1

   template
   copy
