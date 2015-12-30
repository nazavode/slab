# -*- coding: utf-8 -*-

import os

__all__ = (
    'INITPY_FILENAME',
    'SOURCE_SUFFIXES',
    'AUTODOC_OPTIONS',
)

INITPY_FILENAME = '__init__.py'

SOURCE_SUFFIXES = frozenset(['.py', '.pyx'])

# Autodoc options
# Code adapted from the original sphinx.apidoc
if 'SPHINX_APIDOC_OPTIONS' in os.environ:
    __autodoc_options = os.environ['SPHINX_APIDOC_OPTIONS'].split(',')
else:
    __autodoc_options = [
        'members',
        'undoc-members',
        # 'inherited-members', # disabled because there's a bug in sphinx
        'show-inheritance',
    ]

AUTODOC_OPTIONS = __autodoc_options
