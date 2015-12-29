# -*- coding: utf-8 -*-

import argparse
import os

from pyramid.core import build_tree, Module  # TODO
from pyramid.formats import apidoc

__all__ = (
    'main',
)


SUPPORTED_FORMATS = {
    'apidoc': apidoc.ApidocReSTFormat,
}


def argtype_dir_input(arg):
    if not os.path.exists(arg):
        raise argparse.ArgumentTypeError("{} doesn't exist".format(arg))
    elif not os.path.isdir(arg):
        raise argparse.ArgumentTypeError("{} is not a directory".format(arg))
    else:
        return arg


def argtype_dir_output(arg):
        if not os.path.exists(arg):
            os.makedirs(arg)
        elif not os.path.isdir(arg):
            raise argparse.ArgumentTypeError("{} is not a directory".format(arg))
        else:
            return arg


def get_parser(supported_formats):

    def argtype_format(arg):
        if arg not in supported_formats:
            raise argparse.ArgumentTypeError("{} is not a supported format".format(arg))
        return supported_formats[arg]

    parser = argparse.ArgumentParser(description='Process apidoc templates instantiating them in actual ReST files.')
    #
    # Positional arguments
    parser.add_argument('root_dir', type=argtype_dir_input, help='root directory')
    parser.add_argument('excludes', metavar='[exclude_path, ...]', nargs=argparse.REMAINDER)
    #
    # Common options
    parser.add_argument('-o', '--output-dir', dest='destdir', action='store', type=argtype_dir_output,
                        help='Directory to place all output', required=True)
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
    return parser


def main(argv, enabled_formats=SUPPORTED_FORMATS):
    parser = get_parser(enabled_formats)
    args = parser.parse_args(argv[1:])
    # 1. Build element tree
    root = build_tree(args.root_dir)
    # 2. Init output format
    format = args.format(args)
    # 3. Write toc if needed
    if not args.notoc:
        toc = format.toc((root, ))
        with open(os.path.join(args.destdir, args.toc_filename + '.' + args.suffix), 'w') as f:
            f.write(toc)
    # 4. Generate and write all files
    excluded_types = set()
    if not args.separatemodules:  # TODO: this should be Format's responsibility
        excluded_types.add(Module)
    for docitem in root.docitems():
        if docitem.__class__ not in excluded_types:
            content = format.render(docitem)
            if content:
                outfile = os.path.abspath(os.path.join(args.destdir, docitem.qualname + '.' + args.suffix))
                with open(outfile, 'w') as f:
                    f.write(content)


if __name__ == '__main__':
    main(['aaa', '-o', 'PROVA', '/home/fficarelli/Projects/apscheduler/apscheduler'])