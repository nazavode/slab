# -*- coding: utf-8 -*-

import os
import functools

from pyramid.apidoc import apidoc_get_module, apidoc_get_package
from pyramid.utils import is_package, is_source, get_node_name, get_node_qualname, listcontent, is_excluded, \
    get_module_imports


def build_tree(root_path, excludes=None):
    return Directory(root_path, excludes=excludes)


@functools.total_ordering
class Node(object):

    def __init__(self, path, root=None):
        self.path = path
        self.root = root or self.path
        self.name = get_node_name(self.path)
        self.qualname = get_node_qualname(self.path, self.root)
        self.submodules = tuple()
        self.subdirs = tuple()
        self.subpackages = tuple()

    def __lt__(self, other):
        self.qualname.__lt__(other.qualname)

    def __eq__(self, other):
        return self.qualname.__eq__(other.qualname)


class Directory(Node):

    __default_excludes__ = frozenset([
        '__init__.py',
        '__pycache__',
    ])

    def __init__(self, path, root=None, excludes=None):
        super().__init__(path, root)
        self.excludes = excludes or self.__default_excludes__
        files, subdirs = listcontent(self.path)
        self.is_package = is_package(self.path, filelist=files)
        self.submodules = sorted(
                Module(file, self.root) for file in files if is_source(file) and not is_excluded(file, self.excludes)
        )
        self.subdirs = sorted(
            Directory(subdir, self.root, excludes) for subdir in subdirs
            if not is_excluded(subdir, self.excludes)
        )
        self.subpackages = sorted(
            subdir for subdir in self.subdirs if subdir.is_package
        )
        self.is_empty = not self.submodules and not self.subdirs


class Module(Node):

    def __init__(self, path, root=None):
        super().__init__(path, root)
        self.imports = get_module_imports(self.path)


###############################################################################
# Info configuration

def apidoc_get_maker(opts, key='apidoc'):

    def get_apidoc(node):
        if isinstance(node, Directory) and node.is_package:
            return {
                key:
                apidoc_get_package(
                        node,
                        include_submodules=not opts.separatemodules,
                        headings=not opts.noheadings,
                        modulefirst=opts.modulesfirst,
                        apidoc_options=opts.apidoc_options
                )
            }
        elif isinstance(node, Module):
            return {
                key:
                apidoc_get_module(
                        node,
                        headings=not opts.noheadings,
                        apidoc_options=opts.apidoc_options
                )
            }
        else:
            return {}

    return get_apidoc


def template_get_maker(options, key='template'):

    def get_template(node):
        return {
            key: 'TEMPLATE TODO'  # TODO
        }

    return get_template


def outpath_get_maker(options, key='outpath'):

    def get_output_path(node):
        return {
            key: os.path.abspath(os.path.join(options.destdir, node.qualname + '.' + options.suffix))
        }

    return get_output_path


def info_get_maker(options):
    factories = (
        apidoc_get_maker(options),
        template_get_maker(options),
        outpath_get_maker(options),
    )

    def get_info(node):
        info = {}
        for factory in factories:
            info.update(factory(node))
        return info

    return get_info


def dump(root, info_maker, exclude_types=None):

    if exclude_types is None or root.__class__ not in exclude_types:
        info = info_maker(root)
        with open(info['outpath'], 'w') as f:
            f.write(info['apidoc'])

    for subpackage in root.subpackages:
        dump(subpackage, info_maker, exclude_types)

    for submodule in root.submodules:
        dump(submodule, info_maker, exclude_types)