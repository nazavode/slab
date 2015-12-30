# -*- coding: utf-8 -*-

import argparse
import os

from .utils import argtype_dir_input, argtype_dir_output
from .config import AUTODOC_OPTIONS
from .core import build_tree, Module
from .formats import AVAILABLE_FORMATS, format_maker, add_arguments

__all__ = (
    'main',
)


def get_parser(supported_formats):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Process apidoc templates instantiating them in actual ReST files.'
    )
    #
    # Positional arguments
    parser.add_argument('root_dir', type=argtype_dir_input, help='root directory')
    parser.add_argument('excludes', metavar='[exclude_path, ...]', nargs=argparse.REMAINDER)
    #
    # Common options
    parser.add_argument('-o', '--output-dir', dest='destdir', action='store', type=argtype_dir_output,
                        help='Directory to place all output', required=True)
    parser.add_argument('-f', '--force', action='store_true', dest='force', default=False,
                        help='Overwrite existing files')
    #
    # Format options
    add_arguments(parser)
    # Advanced common options
    extra = parser.add_argument_group('Advanced options')
    extra.add_argument('--format',
                       dest='format', default='apidoc', choices=supported_formats,
                       help='Output format.')
    extra.add_argument('--toc-filename',
                       dest='toc_filename', default='modules',
                       help='Toc filename.')
    extra.add_argument('--autodoc-options',
                       dest='autodoc_options', type=list, default=AUTODOC_OPTIONS,
                       help='Sphinx Autodoc options. '
                       'If omitted, the value of environment variable '
                       'SPHINX_APIDOC_OPTIONS will be used.')
    return parser


def main(argv, enabled_formats=AVAILABLE_FORMATS):
    parser = get_parser(enabled_formats)
    args = parser.parse_args(argv[1:])
    # 1. Build element tree
    root = build_tree(args.root_dir)
    # 2. Init output format
    format = format_maker(args.format, args)
    # 3. Write toc if needed
    open_mode = 'x' if args.force else 'w'
    if not args.notoc:
        toc = format.toc((root, ))
        with open(os.path.join(args.destdir, args.toc_filename + '.' + args.suffix), open_mode) as f:
            f.write(toc)
    # 4. Generate and write all files
    excluded_types = set()
    if not args.separatemodules:
        excluded_types.add(Module)
    for docitem in root.docitems():
        if docitem.__class__ not in excluded_types:
            content = format.render(docitem)
            if content:
                outfile = os.path.abspath(os.path.join(args.destdir, docitem.qualname + '.' + args.suffix))
                with open(outfile, open_mode) as f:
                    f.write(content)
