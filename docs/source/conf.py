# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime
import os
import re
import sys
import toml

sys.path.insert(0, os.path.abspath("../../"))

pyproject = toml.load("../../pyproject.toml")
__version__ = pyproject['tool']['poetry']['version']

now = datetime.datetime.now()


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "tinyscaf"
copyright = f"{now.year}, Marcus Robb"
author = "Marcus Robb"

# The full version, including alpha/beta/rc tags
version = __version__  # Built in variable that is displayed above Nav.
project_version = __version__

rst_prolog = f"""
.. |project_version| replace:: {project_version}
"""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinxarg.ext",
    "sphinx.ext.autodoc",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "collapse_navigation": False,
    "display_version": True,
}

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    "css/theme_overrides.css",
]
