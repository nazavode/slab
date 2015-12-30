# -*- coding: utf-8 -*-

import collections

__author__ = 'Federico Ficarelli'
__copyright__ = 'Copyright (c) 2015 Federico Ficarelli'
__license__ = 'Apache License Version 2.0'

__all__ = (
    # Version
    "VERSION_INFO",
    "VERSION",
)

VersionInfo = collections.namedtuple('VersionInfo', (
    'major',
    'minor',
    'patch',
))

VERSION_INFO = VersionInfo(major=0, minor=1, patch=0)

VERSION = '.'.join(str(v) for v in VERSION_INFO)
