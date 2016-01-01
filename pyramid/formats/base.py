# -*- coding: utf-8 -*-

import abc

from ..core import Directory, Module

__all__ = (
    'FormatBase',
)


class FormatBase(metaclass=abc.ABCMeta):

    def __init__(self, options):
        self.configure(options)

    def render(self, item):
        if isinstance(item, Directory) and item.is_package:
            return self.package(item)
        elif isinstance(item, Module):
            return self.module(item)
        else:
            raise TypeError('unknown item type: {}'.format(item.__class__))

    @abc.abstractmethod
    def configure(self, options):
        raise NotImplementedError()

    def module(self, module):
        raise NotImplementedError()

    def package(self, package):
        raise NotImplementedError()

    def toc(self, items):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def add_arguments(cls, parser):
        raise NotImplementedError()


class MetaFormatBase(FormatBase):  # pylint: disable=abstract-method

    def __init__(self, options, format_cls):
        self._format = format_cls(options)
        super().__init__(options)

    @property
    def format(self):
        return self._format
