import logging
import os
import shutil
import sys
from glob import iglob
from pprint import pformat

import nbformat
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from nbconvert import MarkdownExporter

PYTHON_VERSION_MAJOR_MINOR = '{}.{}'.format(*sys.version_info)


class NbConvertPlugin(BasePlugin):

    config_scheme = (
        (
            'input_dir',
            config_options.OptionallyRequired(default='notebooks')
        ), (
            'recursive',
            config_options.OptionallyRequired(default=False)
        ), (
            'output_dir',
            config_options.OptionallyRequired(default='notebooks')
        ),
    )

    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger('mkdocs.plugins.NbConvertPlugin')
        super(NbConvertPlugin, self).__init__(*args, **kwargs)

    def on_files(self, files, config):
        logger = self._logger
        logger.info('nbconvert: plugin config=%s', pformat(self.config))
        # deal with dirs
        config_file_dir = os.path.dirname(config['config_file_path'])
        input_dir = os.path.normpath(self.config['input_dir'])
        output_dir = os.path.realpath(os.path.join(
            config['docs_dir'],
            os.path.normpath(self.config['output_dir'])
        ))
        if not os.path.isabs(input_dir):
            input_dir = os.path.realpath(os.path.join(config_file_dir, input_dir))
        # glob match
        glob_recursive = self.config['recursive'] if PYTHON_VERSION_MAJOR_MINOR >= '3.5' else False
        if glob_recursive:
            nb_paths_iter = iglob(os.path.join(config_file_dir, input_dir, '**', '*.ipynb'), recursive=True)
        else:
            nb_paths_iter = iglob(os.path.join(config_file_dir, input_dir, '*.ipynb'))
        # Exporter
        md_exporter = MarkdownExporter()
        # Converting
        for nb_path in nb_paths_iter:
            # Prepare output file/dir
            nb_dirname, nb_basename = os.path.split(nb_path)
            nb_basename_root, _ = os.path.splitext(nb_basename)
            nb_subdir = os.path.relpath(nb_dirname, input_dir)
            md_dir = os.path.join(output_dir, nb_subdir)
            md_basename = '{0}.md'.format(nb_basename_root)
            md_path = os.path.join(md_dir, md_basename)
            md_rel_dir = os.path.relpath(md_dir, config['docs_dir'])
            md_rel_path = os.path.join(md_rel_dir, md_basename)
            #
            logger.debug('nbconvert: markdown export %s => %s', nb_path, md_path)
            # run nbconvert
            with open(nb_path) as fp:
                nb_node = nbformat.read(fp, nbformat.NO_CONVERT)
            body, resources = md_exporter.from_notebook_node(nb_node)
            # save exported
            if not os.path.exists(md_dir):
                os.makedirs(md_dir)
            with open(md_path, 'w', encoding='UTF8') as fp:
                fp.write(body)
            file_obj = File(
                path=md_rel_path,
                src_dir=config['docs_dir'],
                dest_dir=config['site_dir'],
                use_directory_urls=config['use_directory_urls']
            )

            for resource_name, resource_data in resources['outputs'].items():
                resource_src_dir = os.path.dirname(file_obj.abs_src_path)
                resource_src_path = os.path.join(resource_src_dir, resource_name)
                if not os.path.isdir(resource_src_dir):
                    os.makedirs(resource_src_dir)
                with open(resource_src_path, 'wb') as fp:
                    fp.write(resource_data)
                resource_dest_dir = os.path.dirname(file_obj.abs_dest_path)
                resource_dest_path = os.path.join(resource_dest_dir, resource_name)
                logger.debug('nbconvert: resource output(%dBytes): resource_name --> %s',
                             len(resource_data), resource_dest_path)
                if not os.path.isdir(resource_dest_dir):
                    os.makedirs(resource_dest_dir)
                with open(resource_dest_path, 'wb') as fp:
                    fp.write(resource_data)

            logger.debug(
                'nbconvert: add file object<abs_src_path=%s abs_dest_path=%s url=%s>',
                file_obj.abs_src_path, file_obj.abs_dest_path, file_obj.url
            )
            files.append(file_obj)
        return files

    def on_post_build(self, config):  # pylint:disable=unused-argument
        output_dir = os.path.join(
            config['docs_dir'],
            os.path.normpath(self.config['output_dir'])
        )
        shutil.rmtree(output_dir)
