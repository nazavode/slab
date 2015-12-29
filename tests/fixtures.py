# -*- coding: utf-8 -*-

import os
import itertools
import pytest

from pyramid import *  # this is going to test package's __init__ exports

__all__ = (
    'flags',
    'command',
    'packagedir',
    'pyramid_exe',
)

pyramid_exe = 'pyramid-apidoc'

apidoc_flags = [
    '',
    '--module-first',
    '--separate',
    '--no-headings',
    '--no-toc',
    '--maxdepth=1000',
    '--suffix=TEST',
]

apidoc_test_flags = (
    itertools.chain.from_iterable(
            itertools.combinations(apidoc_flags, r=i) for i in range(len(apidoc_flags))
    )
)

apidoc_commands = [
    ("sphinx", 'sphinx-apidoc'),
]

testpackages = [
    ("testpackage", 'data/testpackage'),
]


@pytest.fixture(params=apidoc_test_flags)
def flags(request):
    return ' '.join(request.param) + ' -o {outdir} {package}'


@pytest.fixture(params=[e[1] for e in apidoc_commands], ids=[e[0] for e in apidoc_commands])
def command(request):
    return request.param


@pytest.fixture(params=[e[1] for e in testpackages], ids=[e[0] for e in testpackages])
def packagedir(request):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), request.param)
