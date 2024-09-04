#!/usr/bin/env python
# coding: utf-8

import re
import os
import subprocess
from setuptools import setup

# Prepare short and long description
description = 'Python API for the Nitrate test case management system'
with open("README.rst") as readme:
    long_description = readme.read()

# Parse version from the spec file
with open("python-nitrate.spec") as specfile:
    lines = "\n".join(line.rstrip() for line in specfile)
    version = re.search('Version: (.+)', lines).group(1).rstrip()

setup(name='nitrate',
      version=version,
      packages=['nitrate'],
      package_dir={'nitrate': 'source'},
      scripts=['source/nitrate'],
      description=description,
      long_description=long_description,
      author='Petr Šplíchal',
      author_email='psplicha@redhat.com',
      license='LGPLv2+',
      install_requires=[
          'gssapi',
          'psycopg; python_version >= "3.13"',
          'psycopg2; python_version < "3.13"',
          'six',
          ],
      url='https://psss.fedorapeople.org/python-nitrate/',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v2' +
        ' or later (LGPLv2+)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
      ])
