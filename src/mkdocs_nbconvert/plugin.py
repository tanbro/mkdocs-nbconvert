import logging
import os
import subprocess
import sys
from glob import iglob

import nbformat
from mkdocs import utils as mkdocs_utils
from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from nbconvert import MarkdownExporter

PYTHON_VERSION_MAJOR_MINOR = '{}.{}'.format(*sys.version_info)


log = logging.getLogger('mkdocs.plugins.NbConvertPlugin')


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
        self._exported_files = []
        return super().__init__(*args, **kwargs)

    def on_files(self, files, config):
        # deal with dirs
        config_file_dir = os.path.dirname(config['config_file_path'])
        input_dir = os.path.normpath(self.config['input_dir'])
        output_dir = os.path.join(
            config['docs_dir'],
            os.path.normpath(self.config['output_dir'])
        )
        if not os.path.isabs(input_dir):
            input_dir = os.path.realpath(
                os.path.join(config_file_dir, input_dir))
        # glob match
        if self.config['recursive'] if PYTHON_VERSION_MAJOR_MINOR >= '3.5' else False:
            nb_file_iter = iglob(
                os.path.join(input_dir, '**', '*.ipynb'),
                recursive=True
            )
        else:
            nb_file_iter = iglob(os.path.join(input_dir, '*.ipynb'))
        # Exporter
        md_exporter = MarkdownExporter()
        # Converting
        for nb_path in nb_file_iter:
            # Prepare output file/dir
            nb_dirname, nb_basename = os.path.split(nb_path)
            nb_basename, _ = os.path.splitext(nb_basename)
            nb_subdir = os.path.relpath(nb_dirname, input_dir)
            md_dir = os.path.realpath(os.path.join(output_dir, nb_subdir))
            md_path = os.path.realpath(os.path.join(
                md_dir, '{0}.md'.format(nb_basename)))
            md_rel_dir = os.path.relpath(md_dir, config['docs_dir'])
            md_rel_path = os.path.relpath(md_path, config['docs_dir'])
            #
            log.debug('nbconvert export notebook %s => %s',
                      nb_path, md_rel_path)
            # run nbconvert
            with open(nb_path) as fp:
                nb = nbformat.read(fp, nbformat.NO_CONVERT)
            body, resources = md_exporter.from_notebook_node(nb)
            # save exported
            if not os.path.exists(md_dir):
                os.makedirs(md_dir)
            with open(md_path, 'w') as fp:
                fp.write(body)
            self._exported_files.append(md_path)
            files.append(File(
                md_rel_path,
                docs_dir,
                config['site_dir'],
                config['use_directory_urls']
            ))

        return files

    def on_post_build(self, config):
        for path in self._exported_files:
            os.remove(path)
