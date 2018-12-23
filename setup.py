#!/usr/bin/env python

from os.path import abspath, dirname, join
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import autoadmin as package

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def read_file(filename):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), filename)) as f:
        return f.read()


setup(
    author=package.__author__,
    author_email=package.__author_email__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description=package.__doc__.strip(),
    include_package_data=True,
    install_requires=read_file('requirements/common.txt').splitlines(),
    license=package.__license__,
    long_description='\n\n'.join([
        read_file('README.rst'),
        read_file('HISTORY.rst'),
    ]),
    name=package.__title__,
    package_data={'': ['LICENSE']},
    package_dir={'autoadmin': 'autoadmin'},
    packages=[
        'autoadmin',
        'autoadmin.migrations',
        'autoadmin.templatetags',
        'autoadmin.management',
        'autoadmin.management.commands',
    ],
    platforms=['any'],
    url=package.__url__,
    version=package.__version__,
    zip_safe=False,
)
