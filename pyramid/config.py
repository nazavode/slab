# -*- coding: utf-8 -*-
"""

"""

import os

__all__ = ()

# Automodule options
# Code adapted from the original sphinx.apidoc
if 'SPHINX_APIDOC_OPTIONS' in os.environ:
    APIDOC_OPTIONS = os.environ['SPHINX_APIDOC_OPTIONS'].split(',')
else:
    APIDOC_OPTIONS = [
        'members',
        'undoc-members',
        # 'inherited-members', # disabled because there's a bug in sphinx
        'show-inheritance',
    ]

INITPY_FILENAME = '__init__.py'

SOURCE_SUFFIXES = frozenset(['.py', '.pyx'])
