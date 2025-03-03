Copy
####

Description
===========

This sub-command copies a selection of tool properties from a reference project
to targets projects. The properties are propagated for all the configurations
they appear in the reference project. A configuration is created in the
target project if needed.

The properties to consider should be specified in a configuration file (JSON):

* keys: Identifiers of the tools
* values: Identifiers of the properties.

  If a property designates a file, that can be relative to the project, prefix
  its identifier with ``@``.

You can derive the configuration file from a template as detailed in this
:doc:`section </user-guide/project-properties/template>`.

.. Note::

    * A tool property is saved in a project file with the name
      ``@<tool>:<property>`` and has a list of values. It is optionally linked
      to a configuration.
    * Properties with default values are not stored in the project files.
    * The identifiers used to store properties in a project file are not
      documented. To find the identifiers, tool and property, corresponding
      to a given setting, you can compare the project files before and after
      modifying this single setting. This may lead to the creation of a new
      property if you override the default, or the deletion of a property if
      you restore its default value.

For example, the following schema corresponds to the `Configuration` settings of KCG:

.. image:: /_static/settings_configuration.png

.. code:: json

   {
       "GENERATOR": [
           "GLOBAL_ROOT_CONTEXT",
           "WRAP_C_OPS",
           "MACRO_ON_ASSERT",
           "PROBES",
           "STATE_VECTOR",
           "NO_BITWISE",
           "NO_TIMESTAMP",
           "GLOBALS_PREFIX",
           "NAME_LENGTH",
           "SIGNIFICANCE_LENGTH",
           "@USER_CONFIG",
           "@HEADER",
       ]
   }

Usage
=====

.. code:: text

   usage: ansys_scade_ps_project_properties copy [-h] -s <schema> [-p <project> [<project> ...]]

   options:
     -h, --help            show this help message and exit
     -s <schema>, --schema <schema>
                           input schema file (JSON)
     -p <project> [<project> ...], --projects <project> [<project> ...]
                           project files to update (ETP)

For example:

.. code:: bash

   ansys_scade_ps_project_properties -p Reference.etp copy -s MySchema.json -p P1.etp P2.etp
