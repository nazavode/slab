# -*- coding: utf-8 -*-
"""

"""

import abc

__all__ = (
    'FormatBase',
)


class FormatBase(metaclass=abc.ABCMeta):

    def __init__(self, options):
        self.configure(options)

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
    def options(cls, parser):
        raise NotImplementedError()
