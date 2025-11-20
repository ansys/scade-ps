"""Sphinx documentation configuration file."""

from datetime import datetime
import os

from ansys_sphinx_theme import (
    ansys_favicon,
    get_version_match,
)

from ansys.scade.ps import __version__

# Project information
project = 'ansys-scade-ps'
copyright = f'(c) {datetime.now().year} ANSYS, Inc. All rights reserved'
author = 'ANSYS, Inc.'
release = version = __version__
switcher_version = get_version_match(version)

# Select desired logo, theme, and declare the html title
html_theme = 'ansys_sphinx_theme'
html_short_title = html_title = 'Ansys SCADE Power Scripts'

# multi-version documentation
cname = os.getenv('DOCUMENTATION_CNAME', 'ps.scade.docs.pyansys.com')
"""The canonical name of the webpage hosting the documentation."""

# specify the location of your github repo
html_theme_options = {
    'github_url': 'https://github.com/ansys/scade-ps',
    'show_prev_next': False,
    'show_breadcrumbs': True,
    'additional_breadcrumbs': [
        ('PyAnsys', 'https://docs.pyansys.com/'),
    ],
    'switcher': {
        'json_url': f'https://{cname}/versions.json',
        'version_match': switcher_version,
    },
    # TODO: remove this after public release
    # https://github.com/ansys/scade-ps/issues/24
    'check_switcher': False,
    'logo': 'pyansys',
}

# Sphinx extensions
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx_design',
]


# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.10', None),
    # kept here as an example
    # "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    # "numpy": ("https://numpy.org/devdocs", None),
    # "matplotlib": ("https://matplotlib.org/stable", None),
    # "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    # "pyvista": ("https://docs.pyvista.org/", None),
    # "grpc": ("https://grpc.github.io/grpc/python/", None),
}

# Favicon
html_favicon = ansys_favicon

# static path
html_static_path = ['_static']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# TODO: remove ignore links after public release
# https://github.com/ansys/scade-ps/issues/24
linkcheck_ignore = [
    'https://github.com/ansys/scade-ps',
    'https://github.com/ansys/scade-ps/actions/workflows/ci_cd.yml',
    'https://pypi.org/project/ansys-scade-ps',
    'https://ansyshelp.ansys.com/*',
    # The link below takes a long time to check
    'https://www.ansys.com/products/embedded-software/ansys-scade-suite',
    'https://www.ansys.com/*',
]

if switcher_version != 'dev':
    linkcheck_ignore.append(f'https://github.com/ansys/scade-ps/releases/tag/v{__version__}')
