# -*- coding: utf-8 -*-

import os
import itertools
import pytest

from pyramid_apidoc import *  # this is going to test package's __init__ exports

pyramid_exe = 'pyramid-apidoc'

apidoc_compatible_templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'templates', 'sphinx-compatible')

apidoc_compatible_format_flags = [
    ('fmtdef', ''),  # default
    ('fmtapi', '--format=apidoc'),
    ('fmttpl', '--format=template-apidoc --templates-dir={}'.format(apidoc_compatible_templates_dir)),
]

apidoc_flags = [
    '',  # all options to defaults
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
    ("cmpsphinx", 'sphinx-apidoc'),
]

testpackages = [
    ("pkgtest", 'data/testpackage'),
]


@pytest.fixture(params=apidoc_test_flags)
def config_flags(request):
    return ' '.join(request.param) + ' -o {outdir} {package}'


@pytest.fixture(params=[e[1] for e in apidoc_compatible_format_flags], ids=[e[0] for e in apidoc_compatible_format_flags])
def format_flags(request):
    return request.param


@pytest.fixture(params=[e[1] for e in apidoc_commands], ids=[e[0] for e in apidoc_commands])
def command(request):
    return request.param


@pytest.fixture(params=[e[1] for e in testpackages], ids=[e[0] for e in testpackages])
def packagedir(request):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), request.param)
