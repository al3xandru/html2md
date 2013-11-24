# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='html2md',
    version='0.1',
    description='An HTML to Markdown converter inspired by Aaron Swartz\'s html2text' ,
    long_description=readme,
    author='Alex Popescu',
    author_email='html2md@mypopescu.com',
    url='https://github.com/al3xandru/html2md',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

