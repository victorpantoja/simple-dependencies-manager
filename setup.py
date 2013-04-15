# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from simple_manager import __version__ as Version

setup(
    name=u'simple-dependencies-manager',
    version=Version,
    description=u"A simple script that helps you take control of your projects so you do not get crazy!",
    long_description=u"A simple script that helps you take control of your projects so you do not get crazy!",
    keywords='dependencies manager git tags requirements',
    author=u'Victor Pantoja',
    author_email='victor.pantoja@gmail.com',
    url='http://github.com/victorpantoja/simple-dependencies-manager',
    license='Apache License 2.0',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python'],
    packages=find_packages(),
    package_dir={"simple_manager": "simple_manager"},
    include_package_data=True,
    scripts=['simple_manager/simple-manager.py'],

    install_requires=[
        "PyYAML==3.10"
    ]
)
