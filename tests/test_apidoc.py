# -*- coding: utf-8 -*-

import os
import filecmp
import subprocess

# NB: due to the discovery mechanism carried out by py.test, we can import test modules
# in the same way as if they were proper modules (even if no __init__.py is present).
# For further details: https://pytest.org/latest/goodpractises.html
from fixtures import *


def test_compare(flags, command, packagedir, tmpdir):
    # Create output directories
    my_outdir = 'pyramid-out' # str(tmpdir.join('pyramid'))
    theirs_outdir = 'compare-out' # str(tmpdir.join('compare'))
    os.makedirs(my_outdir)
    os.makedirs(theirs_outdir)
    # Create command lines
    my_cmdline = 'pyramid-apidoc ' + flags.format(outdir=my_outdir, package=packagedir)
    theirs_cmdline = command + ' ' + flags.format(outdir=theirs_outdir, package=packagedir)
    # Run commands
    subprocess.call(my_cmdline.split())
    subprocess.call(theirs_cmdline.split())
    # Compare
    cmp = filecmp.dircmp(str(my_outdir), str(theirs_outdir))
    assert len(cmp.left_only) == 0
    assert len(cmp.right_only) == 0
    assert len(cmp.funny_files) == 0
    assert len(cmp.diff_files) == 0
    cmp.report_full_closure()
