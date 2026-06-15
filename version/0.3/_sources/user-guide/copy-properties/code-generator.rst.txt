Code Generator
##############

Template: ``code_generator.json``.

.. vale off

General
=======

.. image:: /_static/cg_general.png

Tool: ``GENERATOR``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Root operator
     - ROOTNODE
     -
     - list of scade paths
   * - Code Generator
     - GENERATOR
     -
     - `ADA\  QUAL661`, `ADA\  QUAL663`, `C\  ACG`, `C\  MCG`, `C\  QUAL661`, `C\  QUAL663`
   * - Target directory
     - TARGET_DIR
     - `$(NodeName)_$(CG)`
     -
   * - Set warnings as errors
     - SET_WARNINGS_AS_ERRORS
     - `false`
     -
   * - Skip unused model objects
     - SKIP_UNUSED
     - `false`
     -
   * - Skip disabled model objects
     - SKIP_COMMENTED
     - `false`
     -
   * - Select object(s) to comment
     - COMMENTEDNODES
     -
     - list of scade paths

Expansion
=========

.. image:: /_static/cg_expansion.png

Tool: ``GENERATOR``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Expand
     - EXPAND_MODE
     - `2`
     - `1` (All), `2` (Selected), `3` (All except selected)
   * - Selected
     - EXPANDED_NODES
     -
     - list of scade paths
   * - All except selected
     - NOT_EXPANDED_NODES
     -
     - list of scade paths

Separate I/Os
=============

.. image:: /_static/cg_separate_ios.png

Tool: ``GENERATOR``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Separate I/Os
     - SEP_IO_MODE
     - `6`
     - `1` (All), `6` (Selected), `7` (All except selected)
   * - Selected
     - SEP_IO_NODES
     -
     - list of scade paths
   * - All except selected
     - NO_SEP_IO_NODES
     -
     - list of scade paths

Code Integration
================

.. image:: /_static/cg_code_integration.png

Tool: ``GENERATOR``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - None - Target - Adaptor
     - TARGET_ADAPTOR
     -
     -
   * - Other extensions
     - OTHER_EXTENSIONS
     -
     - list of extension identifiers
   * - Periodicity
     - PERIODICITY_MODE
     - `ROOTNODE`
     - `ROOTNODE`, `USER`, `APERIODIC`
   * - Period
     - PERIODICITY_PERIOD
     - `20`
     -
   * - Offset
     - PERIODICITY_OFFSET
     - `0`
     -
   * - Unit
     - PERIODICITY_UNIT
     - `ms`
     -
   * - User-provided sensors declaration-
     - USER_SENSORS_DECL
     - `false`
     -

Debug
=====

.. image:: /_static/cg_debug.png

Tool: ``GENERATOR``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Debug All
     - DEBUG
     - `false`
     -
   * -
     - OBSERVE_MODE
     - `0`
     - `0` (None), `4` (Selected), `5` (All except selected)
   * - Selected
     - OBSERVED_NODES
     -
     - list of scade paths
   * - All except selected
     - NOT_OBSERVED_NODES
     -
     - list of scade paths

Optimizations
=============

.. image:: /_static/cg_optimizations.png

Tool: ``GENERATOR``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Local variables as static
     - STATIC
     - `false`
     -
   * - Input threshold
     - INPUT_THRESHOLD
     - `0`
     -

Configuration
=============

.. image:: /_static/cg_configuration.png

Tool: ``GENERATOR``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Generate context as global
     - GLOBAL_ROOT_CONTEXT
     - `false`
     -
   * - Wrap C operators
     - WRAP_C_OPS
     - `false`
     -
   * - Keep assertions
     - MACRO_ON_ASSERT
     - `false`
     -
   * - Keep probes in generated code
     - PROBES
     - `false`
     -
   * - Generate system memory state management
     - STATE_VECTOR
     - `false`
     -
   * - Short circuit operators
     - NO_BITWISE
     - `false`
     -
   * - No timestamp
     - NO_TIMESTAMP
     - `false`
     -
   * - Global prefix
     - GLOBALS_PREFIX
     -
     -
   * - Name length
     - NAME_LENGTH
     - `200`
     -
   * - Significance length
     - SIGNIFICANCE_LENGTH
     - `31`
     -
   * - User config
     - USER_CONFIG
     -
     -
   * - Header file
     - HEADER
     -
     -
   * - Top-level package
     - ROOT_PACKAGE
     -
     -
   * - Top-level imported package
     - IMP_ROOT_PACKAGE
     -
     -
   * - Use type clauses
     - USE_TYPES
     -
     - list of type names

Compiler
========

.. image:: /_static/cg_compiler.png

Tool: ``SIMULATOR``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Compiler
     - COMPILER
     - `GNU C`
     -
   * - CPU type
     - CPU_TYPE
     - `win32`
     -

The name of the tool for the renaming properties of this tab are the
concatenation of the name of the selected compiler and CPU type.
For example, the tables hereafter show the most popular ones:

.. image:: /_static/cg_compiler_gnu_c.png

Tool: ``GNU Cwin32`` or ``GNU Cwin64``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Preprocessor definitions
     - PREPROC_DEF
     - `BUILD_DLL`
     -
   * - Additional compiler options
     - ADD_COMP_OPTIONS
     - `-pedantic`
     -
   * - Additional linker options
     - ADD_LINK_OPTIONS
     -
     -

.. image:: /_static/cg_compiler_vs.png

Tool: ``VS2022win32`` or ``VS2022win64``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Preprocessor definitions
     - PREPROC_DEF
     - `_CRT_SECURE_NO_WARNINGS`
     -
   * - Additional compiler options
     - ADD_COMP_OPTIONS
     - `/nologo /O2`
     -
   * - Additional linker options
     - ADD_LINK_OPTIONS
     - `/subsystem:console /nologo /incremental:no`
     -

Build
=====

.. image:: /_static/cg_build.png

Tool: ``COMPILER``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Additional include directories
     - ADD_INCLUDE_DIR
     -
     - list of directories
   * - Excluded files
     - IGNORED_FILES
     -
     - list of files

Simulation
==========

.. image:: /_static/cg_simulation.png

Tool: ``SSMGUI``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - GUI extension files
     - GUIEXTFILE
     -
     - list of files
   * - Enable double simulation
     - DBLSIM
     - `false`
     -
   * - Project
     - DBLSIMPRJ
     -
     -
   * - Configuration
     - DBLSIMCONF
     -
     -

Timing and Stack Analysis Tools
===============================

.. image:: /_static/cg_timing_and_stack_analysis_tools.png

Tool: ``GENERATOR``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Generate loop bounds annotations
     - AIT_GENERATE_ANNOTATIONS
     - `true`
     -
   * - Generate types copy functions
     - AIT_GENERATE_COPY_FUNC
     - `false`
     -

.. vale on
