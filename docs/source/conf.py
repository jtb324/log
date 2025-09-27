# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "modified-logger"
copyright = "2025, J.T. Baker"
author = "J.T. Baker"
release = "2.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
sys.path.insert(0, os.path.abspath("../../src/"))

github_url = "https://github.com/jtb324/log"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_design",
]
pygments_style = "sphinx"

napoleon_google_docstring = True

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
master_doc = "index"

html_theme = "shibuya"
html_theme_options = {
    "github_url": "https://github.com/jtb324/log",
}
html_title = "modified-logger"
# html_static_path = ["_static"]
