#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Topic :: Internet',
    'Topic :: Utilities',
]

settings = dict(
    name='requem',
    version='0.1',
    description='sqlite3 concurrent interface',
    long_description=open('README.rst').read(),
    author='Stefano Dipierro',
    license='Apache 2.0',
    url='https://github.com/dipstef/requem',
    classifiers=CLASSIFIERS,
    keywords='sqlite3 database concurrent threads process ipc remote sql',
    packages = ['requem', 'requem.commands', 'requem.http', 'requem.remote_pool', 'requem.remote_queue',
                'requem.zeromq'],
    test_suite='tests',
    requires=['pyzmq', 'web.py', 'quecco']
)

setup(**settings)