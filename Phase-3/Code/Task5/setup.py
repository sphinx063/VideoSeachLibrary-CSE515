#!/usr/bin/env python
import sys
from setuptools import setup

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
setup_requires = ['pytest-runner>=2.0,<3.0'] if needs_pytest else []

setup(
    name='NearPy',
    version='1.0.0',
    author='Ole Krause-Sparmann',
    author_email='ole@pixelogik.de',
    packages=[
        'nearpymod',
        'nearpymod.distances',
        'nearpymod.experiments',
        'nearpymod.filters',
        'nearpymod.hashes',
        'nearpymod.hashes.permutation',
        'nearpymod.storage',
        'nearpymod.utils'
    ],
    url='https://github.com/pixelogik/NearPy',
    license='LICENSE.txt',
    description='Framework for fast approximated nearest neighbour search.',
    keywords='nearpymod approximate nearest neighbour',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy",
        "scipy",
        "bitarray",
        "future",
    ],
    setup_requires=setup_requires,
    tests_require=[
        "pytest",
        "redis",
        "mockredispy",
    ]
)
