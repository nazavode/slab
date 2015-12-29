# -*- coding: utf-8 -*-
"""

"""

###############################################################################
# Apidoc text rendering - ReST format
# Code adapted from the original sphinx.apidoc

# import

__all__ = ()


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
        text = apidoc_format_heading(1, '{} module'.format(module.name)) + text
    return text


def apidoc_get_modules_toc(modules, header, maxdepth):
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
                text += apidoc_get_module(submodule, headings=False, apidoc_options=apidoc_options) + '\n\n'
        else:
            text += '.. toctree::\n\n' + \
                    '\n'.join('   {}'.format(submodule.qualname) for submodule in package.submodules)

    title = apidoc_format_heading(1, '{} package'.format(package.qualname))
    if modulefirst:
        # Force headings to disabled state as done by apidoc:
        text = title + apidoc_get_module(package, headings=False, apidoc_options=apidoc_options) + '\n' + text
    else:
        # Force headings to disabled state as done by apidoc:
        text = title + text + apidoc_format_heading(2, 'Module contents') + \
               apidoc_get_module(package, headings=False, apidoc_options=apidoc_options)

    return text