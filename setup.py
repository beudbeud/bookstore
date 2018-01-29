#!/usr/bin/python
# -*- coding:Utf-8 -*-

from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst', format='md')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()


setup(name='Bookstore',
      version='0.1',
      description='',
      author='Adrien Beudin',
      long_description=read_md('README.md') + "\n\n\n" + open('docs/changelog.rst').read(),
      author_email='beudbeud@beudibox.fr',
      url='https://github.com/abeudin/bookstore',
      install_requires=open("./requirements.txt", "r").read().split(),
      packages=['bookstore'],
      license= 'GPLv3+',
      include_package_data=True,
      zip_safe=False
)
