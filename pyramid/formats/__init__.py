# -*- coding: utf-8 -*-

from . import (
    apidoc,
    template,
)

__all__ = (
    'AVAILABLE_FORMATS',
    'format_maker',
    'add_arguments',
)


__formats = {
    'apidoc': apidoc.ApidocReSTFormat,
    'template-apidoc': template.TemplateApidocFormat,
}


AVAILABLE_FORMATS = frozenset(__formats.keys())


def add_arguments(parser):
    for cls in __formats.values():
        cls.add_arguments(parser)


def format_maker(format_name, options):
    if format_name in __formats:
        return __formats[format_name](options)
    else:
        raise ValueError('unknown format specifier: {}'.format(format_name))
