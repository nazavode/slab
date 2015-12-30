# -*- coding: utf-8 -*-
"""

"""

###############################################################################
# Apidoc text rendering - ReST format
# Code adapted from the original sphinx.apidoc

import os
import functools

from .base import FormatBase

__all__ = (
    'ApidocReSTFormat',
)


# Automodule options
# Code adapted from the original sphinx.apidoc
if 'SPHINX_APIDOC_OPTIONS' in os.environ:
    APIDOC_OPTIONS = os.environ['SPHINX_APIDOC_OPTIONS'].split(',')
else:
    APIDOC_OPTIONS = [
        'members',
        'undoc-members',
        # 'inherited-members', # disabled because there's a bug in sphinx
        'show-inheritance',
    ]


class ApidocReSTFormat(FormatBase):

    def configure(self, opts):
        self.__pakage_impl = functools.partial(
            apidoc_get_package,
            include_submodules=not opts.separatemodules,
            headings=not opts.noheadings,
            modulefirst=opts.modulesfirst,
            apidoc_options=opts.apidoc_options
        )
        self.__toc_impl = functools.partial(
            apidoc_get_modules_toc,
            header=opts.header,
            maxdepth=opts.maxdepth
        )
        self.__module_impl = functools.partial(
            apidoc_get_module,
            headings=not opts.noheadings,
            apidoc_options=opts.apidoc_options
        )

    def package(self, package):
        return self.__pakage_impl(package)

    def toc(self, items):
        return self.__toc_impl(items)

    def module(self, module):
        return self.__module_impl(module)

    @classmethod
    def add_arguments(cls, parser):
        apidoc = parser.add_argument_group('Apidoc format options', 'Options inherited from sphinx.apidoc command.')
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
        apidoc.add_argument('-H', '--doc-project', action='store', dest='header',
                            help='Project name (default: root module name)')
        apidoc.add_argument('--autodoc-options',
                            dest='apidoc_options', type=set, default=APIDOC_OPTIONS,
                            help='Sphinx Autodoc options. '
                            'If omitted, the value of environment variable '
                            'SPHINX_APIDOC_OPTIONS will be used.')


def apidoc_format_heading(level, text):
    """Create a heading of <level> [1, 2 or 3 supported]."""
    underlining = {
        0: '',
        1: '=',
        2: '-',
        3: '~',
    }
    return '{}\n{}\n\n'.format(text, underlining[level]*len(text))


def apidoc_get_module(module, headings, apidoc_options):
    text = '.. automodule:: {}\n'.format(module.qualname)
    for option in apidoc_options:
        text += '    :{}:\n'.format(option)
    if headings:
        text = apidoc_format_heading(1, '{} module'.format(module.qualname)) + text
    return text


def apidoc_get_modules_toc(modules, header, maxdepth):
    if header is None:
        header = modules[0].qualname
    text = apidoc_format_heading(1, '{}'.format(header)) + '.. toctree::\n'
    if maxdepth is not None:
        text += '   :maxdepth: {}\n\n'.format(maxdepth)
    for module in sorted(modules):
        text += '   {}\n'.format(module.qualname)
    return text


def apidoc_get_package(package, include_submodules, headings, modulefirst, apidoc_options):
    # Init text buffer:
    text = ''
    # build a list of directories that are szvpackages (contain an INITPY file)
    # if there are some package directories, add a TOC for theses subpackages
    if package.subpackages:
        text += apidoc_format_heading(2, 'Subpackages') + '.. toctree::\n\n' + \
                '\n'.join('    {}'.format(subpackage.qualname) for subpackage in package.subpackages) + '\n\n'
    # Build the submodules list:
    if package.submodules:
        text += apidoc_format_heading(2, 'Submodules')
        if include_submodules:
            for submodule in package.submodules:
                if headings:
                    text += apidoc_format_heading(2, '%s module' % submodule.qualname)
                # Force headings to disabled state as done by apidoc:
                text += apidoc_get_module(submodule, headings=False, apidoc_options=apidoc_options)
        else:
            text += '.. toctree::\n\n' + \
                    '\n'.join('   {}'.format(submodule.qualname) for submodule in package.submodules)
        text += '\n\n'
    #
    title = apidoc_format_heading(1, '{} package'.format(package.qualname))
    #
    if modulefirst:
        # Force headings to disabled state as done by apidoc:
        text = title + apidoc_get_module(package, headings=False, apidoc_options=apidoc_options) + '\n' + text
    else:
        # Force headings to disabled state as done by apidoc:
        text = title + text + apidoc_format_heading(2, 'Module contents') + \
               apidoc_get_module(package, headings=False, apidoc_options=apidoc_options)
    return text