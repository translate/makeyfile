#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python makeyfile
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages


install_requires = []
extras_require = {}
extras_require['test'] = [
    "pytest",
    "pytest-mock",
    "requests_mock",
    "coverage",
    "pytest-coverage",
    "codecov",
    "flake8"],

setup(
    name='makeyfile',
    version='0.0.2',
    description='Python Makeyfile',
    long_description="Python makeyfile",
    url='https://github.com/translate/makeyfile',
    author='Ryan Northey',
    author_email='ryan@synca.io',
    license='GPL3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Programming Language :: Python :: 2.7',
    ],
    keywords='python make',
    install_requires=install_requires,
    extras_require=extras_require,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    entry_points={
        'console_scripts': [
            'makey = makeyfile.runner:main',
        ],
    },
    include_package_data=True)
