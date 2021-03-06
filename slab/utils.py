# -*- coding: utf-8 -*-

import ast
import os
import fnmatch
import argparse

from .config import INITPY_FILENAME, SOURCE_SUFFIXES


__all__ = (
    'is_package',
    'is_source',
    'get_node_extension',
    'get_node_name',
    'get_node_qualname',
    'listcontent',
    'is_excluded',
    'get_module_imports',
    'argtype_dir_input',
    'argtype_dir_output',
)


if hasattr(os, 'scandir'):
    # New in Python 3.5, use if available.
    def __listcontent(path):
        subdirs = set()
        files = set()
        for entry in os.scandir(path):  # pylint: disable=no-member
            if entry.is_dir():
                subdirs.add(entry.path)
            else:
                files.add(entry.path)
        return files, subdirs
else:
    # ...otherwise fallback to listdir().
    def __listcontent(path):
        subdirs = set()
        files = set()
        for entry in os.listdir(path):
            entry = os.path.join(path, entry)
            if os.path.isdir(entry):
                subdirs.add(entry)
            else:
                files.add(entry)
        return files, subdirs

listcontent = __listcontent  # pylint: disable=invalid-name


def is_package(path, initfile=INITPY_FILENAME):
    return os.path.isfile(os.path.join(path, initfile))


def is_source(path, suffixes=SOURCE_SUFFIXES):
    return os.path.isfile(path) and get_node_extension(path) in suffixes


def get_node_extension(path):
    return os.path.splitext(os.path.basename(os.path.normpath(path)))[1]


def get_node_name(path):
    return os.path.splitext(os.path.basename(os.path.normpath(path)))[0]


def get_node_qualname(path, root_path):
    return os.path.splitext(os.path.relpath(path, os.path.join(root_path, '..')))[0].replace(os.sep, '.')


def is_excluded(path, excludes):
    return any(fnmatch.fnmatch(os.path.normpath(os.path.basename(path)), pattern) for pattern in excludes)


def get_module_imports(module_file):

    imports = []

    class __visitor(ast.NodeVisitor):  # pylint: disable=invalid-name

        @classmethod
        def repr_alias(cls, alias):
            return str(alias.name) + (' as ' + alias.asname if alias.asname else '')

        @classmethod
        def repr_alias_list(cls, node):
            return ''.join(
                ', ' + cls.repr_alias(alias) for alias in node.names
            ).lstrip(', ')

        def visit_Import(self, node):  # pylint: disable=invalid-name
            imports.append('import {alias_list}'.format(
                alias_list=self.repr_alias_list(node)
            ))

        def visit_ImportFrom(self, node):  # pylint: disable=invalid-name
            imports.append('from {level}{module} import {alias_list}'.format(
                level='.' * node.level,
                module=node.module,
                alias_list=self.repr_alias_list(node)
            ))

        def visit_ClassDef(self, node):  # pylint: disable=invalid-name
            pass  # Cut subtree, we want top-level tokens only.

        def visit_FunctionDef(self, node):  # pylint: disable=invalid-name
            pass  # Cut subtree, we want top-level tokens only.

    with open(module_file, 'r') as infile:
        source = infile.read()
    tree = ast.parse(source)
    __visitor().visit(tree)
    return imports


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
    return arg
