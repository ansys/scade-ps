Set equation sets styles
########################

Rationale
=========

SCADE Suite modeler creates equation sets with the ``Equation Set`` default style,
that makes difficult to identify them. The following diagram has 5 equation sets,
that can be identified one by one, with a double-click.

.. image:: /_static/no_styles.png

It is possible to associate a different style to each equation set: this is a manual and tedious process.

Description
===========

This tool sets a style to equation sets, so that it is unique within a diagram:

* Each equation set is assigned the style ``<prefix><count>`` where
  ``<count>`` starts from 1 and is reset for each diagram, ``<prefix>`` is the
  ``PREFIX`` constant defined at the beginning of the script, the default is ``EQS``.
* The ``<prefix><number>`` styles are not created.
* The equation sets are given a default style if the requested one does
  not exist.
* Existing style assignments are not preserved.

For example, the equation sets of the following diagram have been assigned a different style:

.. image:: /_static/with_styles.png

Usage
=====

The script must be run from the IDE:

* Load ``set_styles.py`` into the IDE.
* Execute ``Tools/Execute script`` command.

It is advised to register it in the menu Tools for a faster access,
cf. ``Tools/Customize...`` command.

The script is located in ``%APPDATA%/Python/Python<version>/site_packages/ansys/scade/ps/set_styles``
directory when the package is installed with recommended options,
otherwise it is installed in the Python distribution you have selected.

Limitations
===========

* The styles must exist else the script makes old versions of SCADE Suite IDE crash.
  For example, if a diagram has eight equation sets, the styles ``EQS1``, ``EQS2``, …, ``EQS8`` must exist.

