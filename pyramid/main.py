# -*- coding: utf-8 -*-
"""

"""

# import
import argparse
import os

from pyramid.config import APIDOC_OPTIONS
from pyramid.core import build_tree, info_get_maker, dump, Module
import pyramid.apidoc as apidoc

__all__ = ()


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

def get_parser():
    parser = argparse.ArgumentParser(description='Process apidoc templates instantiating them in actual ReST files.')

    # Positional arguments
    #
    parser.add_argument('root_dir', type=argtype_dir_input, help='root directory')
    parser.add_argument('excludes', metavar='[exclude_path, ...]', nargs=argparse.REMAINDER)
    #
    apidoc = parser.add_argument_group('Apidoc options', 'Options inherited from sphinx.apidoc command.')
    apidoc.add_argument('-o', '--output-dir', action='store', dest='destdir',
                        help='Directory to place all output', required=True)
    apidoc.add_argument('-E', '--no-headings', action='store_true',
                        dest='noheadings',
                        help='Don\'t create headings for the module/package '
                        'packages (e.g. when the docstrings already contain '
                        'them)')
    apidoc.add_argument('-e', '--separate', action='store_true',
                        dest='separatemodules', default=False,
                        help='Put documentation for each module on its own page')
    apidoc.add_argument('-M', '--module-first', action='store_true',
                        dest='modulesfirst', default=False,
                        help='Put module documentation before submodule '
                        'documentation')
    apidoc.add_argument('-d', '--maxdepth', action='store', dest='maxdepth',
                        help='Maximum depth of submodules to show in the TOC '
                        '(default: 4)', type=int, default=4)
    apidoc.add_argument('-s', '--suffix', action='store', dest='suffix',
                        help='file suffix (default: rst)', default='rst')
    apidoc.add_argument('-T', '--no-toc', action='store_true', dest='notoc',
                        help='Don\'t create a table of contents file', default=False)
    #
    # Extra options
    extra = parser.add_argument_group('Advanced options')
    extra.add_argument('--autodoc-options',
                       dest='apidoc_options', type=set, default=APIDOC_OPTIONS,
                       help='Sphinx Autodoc options. '
                            'If omitted, the value of environment variable '
                            'SPHINX_APIDOC_OPTIONS will be used.')
    extra.add_argument('--toc-filename',
                       dest='toc_filename', default='modules.rst',
                       help='Toc filename.')
    return parser


def main(argv):
    parser = get_parser()
    args = parser.parse_args(argv[1:])
    # 1. Build element tree
    root = build_tree(args.root_dir)
    # print(str_tree(root))

    info_maker = info_get_maker(args)

    if not args.separatemodules:
        no_dump_types = (Module, )
    else:
        no_dump_types = ()

    dump(root, info_maker, no_dump_types)

    if not args.notoc:
        with open(os.path.join(args.destdir, args.toc_filename), 'w') as f:
            f.write(apidoc.apidoc_get_modules_toc((root, ), header=root.name, maxdepth=args.maxdepth))

    # 2. Purge tree from excluded nodes
    # TODO
    # 3. Build info for each node to be documented



if __name__ == '__main__':
    main(['aaa', '-o', '../tests/pyramid', '/home/fficarelli/Projects/apscheduler/apscheduler'])