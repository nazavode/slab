# -*- coding: utf-8 -*-

import ast
import fnmatch
import os

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
)


if hasattr(os, 'scandir'):
    # New in Python 3.5, use if available.
    def __listcontent(path):
        subdirs = set()
        files = set()
        for entry in os.scandir(path):
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

listcontent = __listcontent


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

    class __visitor(ast.NodeVisitor):

        @classmethod
        def repr_alias(cls, alias):
            return str(alias.name) + (' as ' + alias.asname if alias.asname else '')

        @classmethod
        def repr_alias_list(cls, node):
            return ''.join(
                ', ' + cls.repr_alias(alias) for alias in node.names
            ).lstrip(', ')

        def visit_Import(self, node):
            imports.append('import {alias_list}'.format(
                alias_list=self.repr_alias_list(node)
            ))

        def visit_ImportFrom(self, node):
            imports.append('from {level}{module} import {alias_list}'.format(
                level='.' * node.level,
                module=node.module,
                alias_list=self.repr_alias_list(node)
            ))

        def visit_ClassDef(self, node):
            pass  # Cut subtree, we want top-level tokens only.

        def visit_FunctionDef(self, node):
            pass  # Cut subtree, we want top-level tokens only.

    with open(module_file) as f:
        source = f.read()
    tree = ast.parse(source)
    __visitor().visit(tree)
    return imports
