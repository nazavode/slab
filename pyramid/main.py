# -*- coding: utf-8 -*-

import argparse
import os

from .utils import argtype_dir_input, argtype_dir_output
from .config import AUTODOC_OPTIONS
from .core import build_tree, Module  # TODO
from .formats import apidoc, template

__all__ = (
    'main',
)


SUPPORTED_FORMATS = {
    'apidoc': apidoc.ApidocReSTFormat,
    'template': template.TemplateMetaFormat,
}


def get_parser(supported_formats):

    def argtype_format(arg):
        if arg not in supported_formats:
            raise argparse.ArgumentTypeError("{} is not a supported format".format(arg))
        return supported_formats[arg]

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
    for format_cls in supported_formats.values():
        format_cls.add_arguments(parser)
    # Advanced common options
    extra = parser.add_argument_group('Advanced options')
    extra.add_argument('--format',
                       dest='format', type=argtype_format, default='apidoc', choices=supported_formats.keys(),
                       help='Output format.')
    extra.add_argument('--toc-filename',
                       dest='toc_filename', default='modules',
                       help='Toc filename.')
    extra.add_argument('--autodoc-options',
                       dest='autodoc_options', type=set, default=AUTODOC_OPTIONS,
                       help='Sphinx Autodoc options. '
                       'If omitted, the value of environment variable '
                       'SPHINX_APIDOC_OPTIONS will be used.')
    return parser


def main(argv, enabled_formats=SUPPORTED_FORMATS):
    parser = get_parser(enabled_formats)
    args = parser.parse_args(argv[1:])
    # 1. Build element tree
    root = build_tree(args.root_dir)
    # 2. Init output format
    format = args.format(args)
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
