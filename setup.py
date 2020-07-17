#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

setup(
    name='mkdocs-nbconvert',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    license='MIT',
    description='A MkDocs plug-in provides a source parser for *.ipynb files',
    url='https://tanbro.github.io/mkdocs-nbconvert',
    project_urls={
        "Documentation": "https://tanbro.github.io/mkdocs-nbconvert",
        "Source Code": "https://github.com/tanbro/mkdocs-nbconvert"
    },
    long_description=(os.linesep*2).join(
        io.open(file_name, encoding='utf-8').read()
        for file_name in (
            'README.md', 'CHANGELOG.md', 'CONTRIBUTING.md', 'AUTHORS.md'
        )
    ),
    long_description_content_type='text/markdown',
    keywords='mkdocs mkdocs-plugin jupyter-notebook markdown nbconvert'.split(),
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=['mkdocs', 'nbconvert'],
    entry_points={
        'mkdocs.plugins': ['nbconvert = mkdocs_nbconvert:NbConvertPlugin']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
    use_scm_version={
        'version_scheme': 'guess-next-dev',  # guess-next-dev/post-release
        'write_to': 'src/mkdocs_nbconvert/version.py'
    }
)
