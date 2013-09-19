#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

from setuptools import setup

from os.path import abspath, dirname, join

PROJECT_ROOT = abspath(dirname(__file__))
with open(join(PROJECT_ROOT, 'README.rst')) as f:
    readme = f.read()

with open(join(PROJECT_ROOT, 'skiplistcollections.py')) as f:
    version_line = [line for line in f.readlines() if line.startswith('__version__')][0]
    version = version_line.split('=')[1].strip().strip("'")


if __name__ == '__main__':
    setup(
        name='skiplistcollections',
        version=version,
        description='Skip list based sorted collections',
        long_description=readme,
        author='Jakub Stasiak',
        url='https://github.com/jstasiak/skiplistcollections',
        author_email='jakub@stasiak.at',
        py_modules=['skiplistcollections'],
        license='MIT',
        zip_safe=False,
        install_requires=('six',),
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development :: Testing',
            'Topic :: Software Development :: Libraries',
            'Topic :: Utilities',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
        ],
    )
