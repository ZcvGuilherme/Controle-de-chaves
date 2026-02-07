import os
import sys
import django

sys.path.insert(0, os.path.abspath('../../'))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chaves.settings')
django.setup()




# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sistema de Controle de Chaves'
copyright = '2026, Guilherme Sousa, John Victor, Wellington Carvalho, Valfredo Costa, Waldeney Rodrigues'
author = 'Guilherme Sousa, John Victor, Wellington Carvalho, Valfredo Costa, Waldeney Rodrigues'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',          # Puxa docstrings
    'sphinx.ext.napoleon',         # Google/Numpy style
    'sphinx.ext.viewcode',         # Link pro código fonte
    'sphinx.ext.todo',             # Blocos TODO
]

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

autoclass_content = 'both'  # Docstring da classe + __init__

templates_path = ['_templates']
exclude_patterns = []

language = 'pt'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
