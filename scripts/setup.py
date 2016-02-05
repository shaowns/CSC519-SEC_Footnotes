#!/usr/bin/python

from setuptools import setup

setup(name='sec_ftp_fetch',
      version='1.0',
      description='parse SEC document from their ftp server',
      url='http://github.com/shaowns/CSC519-SEC_Footnotes',
      author='rapidwein',
      author_email='rapidwein@gmail.com',
      license='MIT',
      install_requires=[
	'beautifulsoup4',
	],
      zip_safe=False)
