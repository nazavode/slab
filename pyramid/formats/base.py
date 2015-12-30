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
        # TODO: make visitor
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
