# -*- coding: utf-8 -*-

import os
import filecmp
import subprocess

# NB: due to the discovery mechanism carried out by py.test, we can import test modules
# in the same way as if they were proper modules (even if no __init__.py is present).
# For further details: https://pytest.org/latest/goodpractises.html
from fixtures import *


def test_compare(config_flags, format_flags, command, packagedir, tmpdir):
    # Create output directories
    my_outdir = str(tmpdir.join('pyramid'))
    theirs_outdir = str(tmpdir.join('compare'))
    os.makedirs(my_outdir)
    os.makedirs(theirs_outdir)
    # Create command lines
    my_cmdline = pyramid_exe + ' ' + format_flags + ' ' + config_flags.format(outdir=my_outdir, package=packagedir)
    theirs_cmdline = command + ' ' + config_flags.format(outdir=theirs_outdir, package=packagedir)
    # Run commands
    assert subprocess.call(my_cmdline.split()) == 0
    assert subprocess.call(theirs_cmdline.split()) == 0
    # Compare
    cmp = filecmp.dircmp(my_outdir, theirs_outdir)
    assert len(cmp.left_only) == 0
    assert len(cmp.right_only) == 0
    assert len(cmp.funny_files) == 0
    assert len(cmp.diff_files) == 0

