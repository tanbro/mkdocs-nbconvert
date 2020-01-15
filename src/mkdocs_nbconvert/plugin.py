import logging
import os
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
        self._exported_paths = []
        super(NbConvertPlugin, self).__init__(*args, **kwargs)

    def on_files(self, files, config):
        logger = self._logger
        logger.info('nbconvert: plugin config=%s', pformat(self.config))
        # deal with dirs
        config_file_dir = os.path.dirname(config['config_file_path'])
        input_dir = os.path.normpath(self.config['input_dir'])
        output_dir = os.path.join(
            config['docs_dir'],
            os.path.normpath(self.config['output_dir'])
        )
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
            md_dir = os.path.realpath(os.path.join(output_dir, nb_subdir))
            md_basename = '{0}.md'.format(nb_basename_root)
            md_path = os.path.join(md_dir, md_basename)
            md_rel_dir = os.path.relpath(md_dir, config['docs_dir'])
            md_rel_path = os.path.join(md_rel_dir, md_basename)
            #
            logger.info('nbconvert: markdown export %s => %s', nb_path, md_path)
            # run nbconvert
            with open(nb_path) as fp:
                nb_node = nbformat.read(fp, nbformat.NO_CONVERT)
            body, resources = md_exporter.from_notebook_node(nb_node)  # pylint:disable=unused-variable
            # save exported
            if not os.path.exists(md_dir):
                os.makedirs(md_dir)
            with open(md_path, 'w', encoding='UTF8') as fp:
                fp.write(body)
            self._exported_paths.append(md_path)
            file_obj = File(
                path=md_rel_path,
                src_dir=config['docs_dir'],
                dest_dir=config['site_dir'],
                use_directory_urls=config['use_directory_urls']
            )
            logger.info(
                'nbconvert: add file object<abs_src_path=%s abs_dest_path=%s url=%s>',
                file_obj.abs_src_path, file_obj.abs_dest_path, file_obj.url
            )
            files.append(file_obj)
        return files

    def on_post_build(self, config):  # pylint:disable=unused-argument
        for path in self._exported_paths:
            os.remove(path)
