import os
import sys
from unittest.mock import MagicMock

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('../../'))

# -- Mock MCDR ---------------------------------------------------------------
mcd = MagicMock()
sys.modules["mcdreforged"] = mcd
sys.modules["mcdreforged.api.all"] = mcd
sys.modules["mcdreforged.plugin.si.server_interface"] = mcd
mcd.ServerInterface.psi.return_value = MagicMock()

# -- Project information -----------------------------------------------------
project = 'LocationAPI'
copyright = '2026, Mooling'
author = 'Mooling'
version = '0.3.0'
release = '0.3.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'
locale_dirs = ['locale/']   # path is relative to conf.py
gettext_compact = False     # optional.


# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Autodoc configuration ---------------------------------------------------
autodoc_member_order = 'bysource'
autoclass_content = 'both'
