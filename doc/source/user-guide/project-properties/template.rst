Template
########

Description
===========

This sub-command lists all the tool properties used in a project to a file (JSON).

This file can be used as a template for creating a schema of properties to
consider, when :doc:`propagating </user-guide/project-properties/copy>` the
settings from a reference project to other projects.

For a SCADE Suite project with default settings, the output template file looks as follows:

.. code::

   {
       "GENERATOR": [
           "DEBUG",
           "ENABLE_EXTENSIONS",
           "GENERATOR",
           "PROBES",
           "ROOTNODE",
           "SKIP_UNUSED",
           "TARGET_ADAPTOR",
           "TARGET_DIR",
           "USER_CONFIG",
           "USE_TYPES"
       ],
       "METRICS_RULES": [
           "USER_DEF_FILES"
       ],
       "REPORTER": [
           ...
       ],
       ...
   }

.. Note::

   Properties with default values are not stored in the project file: They
   are not listed in the output template.

Usage
=====

.. code:: text

   usage: ansys_scade_ps_project_properties template [-h] -o <template file>

   Ansys SCADE Power Scripts: Access to SCADE project properties

   options:
     -h, --help            show this help message and exit
     -o <template file>, --output <template file>
                           output template file

For example:

.. code:: bash

   ansys_scade_ps_project_properties -p MyProject.etp template -o MyTemplate.json
