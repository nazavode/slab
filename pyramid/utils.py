# -*- coding: utf-8 -*-

import ast
import fnmatch
import os

from .config import INITPY_FILENAME, SOURCE_SUFFIXES


__all__ = ()


def is_package(path, filelist=None, initfile=INITPY_FILENAME):
    if not os.path.isdir(path):
        return False
    if filelist is None:
        filelist = os.listdir(path)
    return initfile in (os.path.basename(filename) for filename in filelist)


def is_source(path, suffixes=SOURCE_SUFFIXES):
    return os.path.isfile(path) and \
           get_node_extension(path) in suffixes


def get_node_extension(path):
    return os.path.splitext(os.path.basename(os.path.normpath(path)))[1]


def get_node_name(path):
    return os.path.splitext(os.path.basename(os.path.normpath(path)))[0]


def get_node_qualname(path, root_path):
    return os.path.splitext(os.path.relpath(path, os.path.join(root_path, '..')))[0].replace(os.sep, '.')


def listcontent(path):
    subdirs = set()
    files = set()
    for entry in os.scandir(path):
        if entry.is_dir():
            subdirs.add(entry.path)
        else:
            files.add(entry.path)
    return files, subdirs
g

def is_excluded(path, excludes):
    return any(fnmatch.fnmatch(os.path.normpath(os.path.basename(path)), pattern) for pattern in excludes)


def get_module_imports(module_file):

    class TopLevelImportsVisitor(ast.NodeVisitor):

        def __init__(self, store):
            self._store = store

        @classmethod
        def repr_alias(cls, alias):
            return str(alias.name) + (' as ' + alias.asname if alias.asname else '')

        @classmethod
        def repr_alias_list(cls, node):
            return ''.join(
                ', ' + cls.repr_alias(alias) for alias in node.names
            ).lstrip(', ')

        def visit_Import(self, node):
            self._store.append('import {alias_list}'.format(
                alias_list=self.repr_alias_list(node)
            ))

        def visit_ImportFrom(self, node):
            self._store.append('from {level}{module} import {alias_list}'.format(
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
    imports = []
    TopLevelImportsVisitor(imports).visit(tree)
    return imports


def str_tree(node, level=0):
    return '{}[{}]\n'.format('  '*level, node.qualname) + \
           ''.join(['{}{}\n'.format('  '*(level+1), subfile.qualname) for subfile in node.submodules]) + \
           ''.join([str_tree(subnode, level+1) for subnode in node.subdirs])