from setuptools import find_packages, setup

setup(
    name='mkdocs-nbconvert',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='liu xue yan',
    author_email='liu_xue_yan@foxmail.com',
    license='MIT',
    description='A MkDocs plug-in provides a source parser for *.ipynb files',
    url='https://github.com/tanbro/mkdocs-nbconvert',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    keywords='mkdocs',
    python_requires='>=3.4',
    install_requires=[
        'mkdocs<2.0,>=1.0.4',
    ],
    # entry_points={
    #     'mkdocs.plugins': [
    #         'mkdocs-nbconvert = mkdocs_nbconvert.plugin:NbConvertPlugin'
    #     ]
    # },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    setup_requires=[
        'setuptools_scm',
        'setuptools_scm_git_archive',
    ],
    use_scm_version={
        'version_scheme': 'guess-next-dev',  # guess-next-dev/post-release
        'write_to': 'src/mkdocs_nbconvert/version.py',
    },
)
