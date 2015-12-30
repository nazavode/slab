# -*- coding: utf-8 -*-

from ..utils import argtype_dir_input, get_module_imports

from .base import MetaFormatBase
from .apidoc import ApidocReSTFormat

__all__ = (
    'TemplateMetaFormat',
    'TemplateApidocFormat',
)


class TemplateMetaFormat(MetaFormatBase):

    def configure(self, options):
        try:
            import jinja2
        except ImportError as err:
            raise ImportError(
                'Can\'t find the jinja2 package, please install it to use {}'.format(self.__class__.__name__)) from err
        # Extract configuration options
        override = not options.no_override
        template_extension = options.template_extension
        templates_dir = options.templates_dir
        # Setup search environment
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=templates_dir))
        # Setup default templates
        module_template = env.get_template(options.module_template.format(TEMPLATE_EXT=template_extension))
        package_template = env.get_template(options.package_template.format(TEMPLATE_EXT=template_extension))
        toc_template = env.get_template(options.toc_template.format(TEMPLATE_EXT=template_extension))
        #
        # Setup override closures

        def __maker(default_template):
            def __get_template(node):
                if not override:
                    return default_template
                else:
                    try:
                        template = env.get_template(node.qualname + template_extension)
                    except jinja2.TemplateNotFound:
                        template = default_template
                    finally:
                        return template  # pylint: disable=lost-exception
            return __get_template

        self.__get_module_template = __maker(module_template)
        self.__get_package_template = __maker(package_template)
        self.__get_toc_template = lambda items, default_template=toc_template: default_template


    def __get_values(self, item):
        return {
            'content': self.format.render(item),
            'name': item.name,
            'qualname': item.qualname,
            'path': item.path,
            'root': item.root,
        }

    def package(self, package):
        return self.__get_package_template(package).render(self.__get_values(package))

    def module(self, module):
        values = self.__get_values(module)
        values['imports'] = get_module_imports(module.path)
        return self.__get_module_template(module).render(values)

    def toc(self, items):
        return self.__get_toc_template(items).render(content=self.format.toc(items))

    @classmethod
    def add_arguments(cls, parser):
        group = parser.add_argument_group('Template options')
        group.add_argument(
            '-X', '--templates-dir',
            metavar='TEMPLATES_DIR',
            dest='templates_dir', type=argtype_dir_input, default='.',
            help='The directory to be searched for template files.'
        )
        group.add_argument(
            '-K', '--template-extension',
            metavar='TEMPLATE_EXT',
            dest='template_extension', default='template',
            help='The extension to be used when looking for override files.'
        )
        group.add_argument(
            '-P', '--package-template',
            dest='package_template', default='package.{TEMPLATE_EXT}',
            help='The template file to be used for all package files generation. '
                 'If a relative path is provided, the file name will be searched in TEMPLATES_DIR.'
        )
        group.add_argument(
            '-D', '--module-template',
            dest='module_template', default='module.{TEMPLATE_EXT}',
            help='The template file to be used for all module files generation. '
                 'If a relative path is provided, the file name will be searched in TEMPLATES_DIR.'
        )
        group.add_argument(
            '-C', '--toc-template',
            dest='toc_template', default='toc.{TEMPLATE_EXT}',
            help='The template file to be used for all TOC files generation. '
                 'If a relative path is provided, the file name will be searched in TEMPLATES_DIR.'
        )
        group.add_argument(
            '-W', '--no-override',
            dest='no_override', action='store_true', default=False,
            help='Disables the template overriding behaviour. '
                 'When specified, only common templates will be used for generation of each file type.'
        )


class TemplateApidocFormat(TemplateMetaFormat):

    def __init__(self, options):
        super().__init__(options, ApidocReSTFormat)
