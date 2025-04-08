Find duplicate OIDs
###################

Description
===========

This sub-command lists the duplicated OIDs for a set of projects.
There is one output file per project, that can be reviewed, and used as input
for the :doc:`command </user-guide/change-oids/new>` that performs the
changes for a project.

The output file is the project's path with a different extension, ``.dupoids.txt``
by default.

Usage
=====

.. code:: text

   usage: ansys_scade_ps_change_oids find [-h] -p <project> [<project> ...] [-x <extension>] [-d]

   options:
     -h, --help            show this help message and exit
     -p <project> [<project> ...], --projects <project> [<project> ...]
                           SCADE Suite projects
     -x <extension>, --extension <extension>
                           result file extension
     -d, --dump_paths      print model element paths

For example:

.. code:: bash

   ansys_scade_ps_change_oids find -p P1/P1.etp P2/P2.etp -d

This command lists the duplicated OIDs of ``P2/P2.etp`` to ``P2/P2.dupoids.txt``,
with path information, for example:

.. code:: text

   !ed/ab/6461/600C/67c802957b40	MyPackage::
   !ed/b8/6461/600C/67c802ab52e2	MyPackage::SOME_CONSTANT/
   !ed/c1/6461/600C/67c802b54ee5	MyOperator/
