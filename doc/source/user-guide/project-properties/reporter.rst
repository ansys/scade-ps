Reporter
########

Template: ``reporter.json``.

.. vale off

General
=======

.. image:: /_static/r_general.png

Tool: ``REPORTER``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Output file
     - DOCUMENT
     - `<project name>.<format>`
     -
   * - Reporter script
     - SCRIPT
     - `Reporter/ScadeReport.tcl`
     -
   * - Format
     - FORMAT
     - `html`
     - `html`, `rtf`

Structure
=========

.. image:: /_static/r_structure.png

Tool: ``REPORTER``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Generate cover, TOC, and first section
     - ReportStructure
     - `true`
     -
   * - Generate list of figures
     - ReportListOfFigures
     - `true`
     -
   * - Generate headers/Footers
     - ReportHeaderAndFooter
     - `true`
     -
   * - Generate list of tables
     - ReportListOfTables
     - `true`
     -
   * - In-line images
     - ImagesInLineWithText
     - `true`
     -
   * - Issue number
     - IssueNr
     - `&lt;issue number&gt;`
     -
   * - Reference number
     - ReferenceNr
     - `&lt;reference number&gt;`
     -
   * - Corporate logo
     - CorporateLogo
     -
     -
   * - SCADE Display co-report
     - SCADEDisplayReport
     - `Complete`
     - `Complete`, `Connection Tables`, `None`
   * - Conf
     - SCADEDisplayReportConf
     -
     -

Cover
=====

.. image:: /_static/r_cover.png

Tool: ``REPORTER``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Document classification
     - Classification
     - `&lt;document classification&gt;`
     -
   * - Distribution list
     - Distribution
     - `&lt;distribution list&gt;`
     -
   * - Image file
     - Image
     -
     -
   * - Report summary
     - Summary
     - `&lt;summary&gt;`
     -

Project Description
===================

.. image:: /_static/r_project_description.png

Tool: ``REPORTER``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Project title
     - Title
     - `$(ProjectTitle)`
     -
   * - Project sub-title
     - Subtitle
     - `$(ProjectSubtitle)`
     -
   * - Project description
     - Description
     - `$(ProjectDescription)`
     -

Document
========

.. image:: /_static/r_document.png

Tool: ``REPORTER``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Company info
     - CompanyInfo
     - `$(ProjectCompanyInfo)`
     -
   * - Authors
     - Authors
     - `$(ProjectAuthors)`
     -
   * - Project reference
     - Reference
     - `$(ProjectReference)`
     -
   * - Project index
     - Index
     - `$(ProjectIndex)`
     -
   * - Project date
     - Date
     - `$(ProjectDate)`
     -

Header/Footer
=============

.. image:: /_static/r_header_footer.png

Tool: ``REPORTER``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Header
     - Header
     - `$(ReferenceNr)&#xA;$(CreatedDate)`, `$(IssueNr)`, `$(PageNumbering)`
     - list of 3 values: left, center, and right
   * - Footer
     - Footer
     - , `&lt;Corporate Info&gt;x`,
     - list of 3 values: left, center, and right

Display
=======

.. image:: /_static/r_display.png

Tool: ``REPORTER``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Display operator calls with context
     - DisplayCtx
     - `false`
     -
   * - Display called and calling operators sections
     - DisplayCalledAndCalling
     - `false`
     -
   * - Display variable usage context
     - DisplayVarCtx
     - `false`
     -
   * - Display KCG and ASAM pragma
     - DisplayKCGPragma
     - `false`
     -
   * - Display requirement description
     - DisplayReqDescr
     - `true`
     -
   * - Allow row to break across page
     - AllowRowToBreak
     - `false`
     -
   * - Diagrams representation
     - diagDisplayType
     - `Normal`
     - `Normal`, `Land`, `Fit`
   * - Constants representation
     - cstDisplayType
     - `Array`
     - `Array`, `View`, `Flat`
   * - Rotate landscape images
     - RotateLandscape
     - `false`
     -

Libraries
=========

.. image:: /_static/r_libraries.png

Tool: ``REPORTER``

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Settings
     - Prop
     - Default
     - Comment
   * - Include libraries
     - LIBRARIES
     - `false`
     -
   * - Selected libraries
     - LibrariesList
     -
     - list of files

.. vale on
