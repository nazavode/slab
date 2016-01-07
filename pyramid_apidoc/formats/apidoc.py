# -*- coding: utf-8 -*-

import functools

from .base import FormatBase

__all__ = (
    'ApidocReSTFormat',
)


class ApidocReSTFormat(FormatBase):

    def configure(self, opts):
        self.__pakage_impl = functools.partial(
            render_package,
            include_submodules=not opts.separatemodules,
            headings=not opts.noheadings,
            modulefirst=opts.modulesfirst,
            autodoc_options=opts.autodoc_options
        )
        self.__toc_impl = functools.partial(
            render_toc,
            header=opts.header,
            maxdepth=opts.maxdepth
        )
        self.__module_impl = functools.partial(
            render_module,
            headings=not opts.noheadings,
            autodoc_options=opts.autodoc_options
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
        apidoc.add_argument(
            '-E', '--no-headings',
            action='store_true', dest='noheadings', default=False,
            help='don\'t create headings for the module/package '
                 'packages (e.g. when the docstrings already contain '
                 'them)'
        )
        apidoc.add_argument(
            '-e', '--separate',
            action='store_true', dest='separatemodules', default=False,
            help='put documentation for each module on its own page'
        )
        apidoc.add_argument(
            '-M', '--module-first',
            action='store_true', dest='modulesfirst', default=False,
            help='put module documentation before submodule '
                 'documentation'
        )
        apidoc.add_argument(
            '-d', '--maxdepth',
            dest='maxdepth', type=int, default=4,
            help='maximum depth of submodules to show in the TOC'
        )
        apidoc.add_argument(
            '-s', '--suffix',
            dest='suffix', default='rst',
            help='output file suffix'
        )
        apidoc.add_argument(
            '-T', '--no-toc',
            action='store_true', dest='notoc', default=False,
            help='don\'t create a table of contents file'
        )
        apidoc.add_argument(
            '-H', '--doc-project',
            dest='header',
            help='Project name (default: root module name)'
        )


def format_heading(level, text):
    """Create a heading of <level> [1, 2 or 3 supported]."""
    underlining = {
        0: '',
        1: '=',
        2: '-',
        3: '~',
    }
    return '{}\n{}\n\n'.format(text, underlining[level] * len(text))


def render_module(module, headings, autodoc_options):
    text = '.. automodule:: {}\n'.format(module.qualname)
    for option in autodoc_options:
        text += '    :{}:\n'.format(option)
    if headings:
        text = format_heading(1, '{} module'.format(module.qualname)) + text
    return text


def render_toc(modules, header, maxdepth):
    if header is None:
        header = modules[0].qualname
    text = format_heading(1, '{}'.format(header)) + '.. toctree::\n'
    if maxdepth is not None:
        text += '   :maxdepth: {}\n\n'.format(maxdepth)
    for module in sorted(modules):
        text += '   {}\n'.format(module.qualname)
    return text


def render_package(package, include_submodules, headings, modulefirst, autodoc_options):
    # Init text buffer:
    text = ''
    # build a list of directories that are szvpackages (contain an INITPY file)
    # if there are some package directories, add a TOC for theses subpackages
    if package.subpackages:
        text += format_heading(2, 'Subpackages') + '.. toctree::\n\n' + \
            '\n'.join('    {}'.format(subpackage.qualname)  # pylint: disable=no-member
                      for subpackage in package.subpackages) + '\n\n'
    # Build the submodules list:
    if package.submodules:
        text += format_heading(2, 'Submodules')
        if include_submodules:
            for submodule in package.submodules:
                if headings:
                    text += format_heading(2, '%s module' % submodule.qualname)
                # Force headings to disabled state as done by apidoc:
                text += render_module(submodule, headings=False, autodoc_options=autodoc_options)
        else:
            text += '.. toctree::\n\n' + \
                    '\n'.join('   {}'.format(submodule.qualname)  # pylint: disable=no-member
                              for submodule in package.submodules)
        text += '\n\n'
    #
    title = format_heading(1, '{} package'.format(package.qualname))
    #
    if modulefirst:
        # Force headings to disabled state as done by apidoc:
        text = title + render_module(package, headings=False, autodoc_options=autodoc_options) + '\n' + text
    else:
        # Force headings to disabled state as done by apidoc:
        text = title + text + format_heading(2, 'Module contents') + \
            render_module(package, headings=False, autodoc_options=autodoc_options)
    return text
