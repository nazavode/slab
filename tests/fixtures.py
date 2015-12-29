# -*- coding: utf-8 -*-

import os

import pytest

from pyramid import *  # this is going to test package's __init__ exports

__all__ = (
    'flags',
    'command',
    'packagedir',
)

apidoc_command_lines = [
    ("simple", '-o {outdir} {package}'),
]

apidoc_commands = [
    ("sphinx", 'sphinx-apidoc'),
]

testpackages = [
    ("testpackage", 'data/testpackage'),
]


@pytest.fixture(params=[e[1] for e in apidoc_command_lines], ids=[e[0] for e in apidoc_command_lines])
def flags(request):
    return request.param


@pytest.fixture(params=[e[1] for e in apidoc_commands], ids=[e[0] for e in apidoc_commands])
def command(request):
    return request.param


@pytest.fixture(params=[e[1] for e in testpackages], ids=[e[0] for e in testpackages])
def packagedir(request):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), request.param)
