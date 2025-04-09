Metrics and Rules Checker
#########################

Template: ``metrics_and_rules_checker.json``.

.. vale off

Model
=====

.. image:: /_static/mr_model.png

Tool: ``METRICS_RULES``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Use selected objects below
     - SELECTED_ROOTS
     -
     - list of scade paths, or empty for all
   * -
     - SELECTED_NODES
     -
     - list of scade paths enclosed by `{}` and suffixed by `/[SELF]`
   * - Use current selection
     - CHECK_ROOTS
     - `false`
     -

Metrics
=======

.. image:: /_static/mr_metrics.png

Tool: ``METRICS_RULES``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * -
     - SELECTED_METRICS
     -
     - list of metric identifiers

Rules
=====

.. image:: /_static/mr_rules.png

Tool: ``METRICS_RULES``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * -
     - SELECTED_RULES
     -
     - list of rule identifiers
   * -
     - RULES_PARAM
     -
     - list of rule parameters, encoded as `<ID>,<PARAM>`

Manage metrics and rules
========================

.. image:: /_static/mr_metrics_and_rules.png

Tool: ``METRICS_RULES``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Defined in files
     - USER_DEF_FILES
     -
     - list of files

.. vale on
