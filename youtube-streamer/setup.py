#!/usr/bin/env python3

from setuptools import setup

setup(
    name='config',
    description='config for youtube-streamer',
    author='Didier Roche <didier.roche@canonical.com>',
    license='GPLv3',
    install_requires=[
        'pyyaml',
    ],
    scripts=[
        'config.py',
    ],
)
