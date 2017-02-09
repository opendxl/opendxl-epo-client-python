from setuptools import setup
import distutils.command.sdist

from pkg_resources import Distribution
from distutils.dist import DistributionMetadata
import setuptools.command.sdist

# Patch setuptools' sdist behaviour with distutils' sdist behaviour
setuptools.command.sdist.sdist.run = distutils.command.sdist.sdist.run

VERSION = __import__('dxlepoclient').get_version()

dist = setup(
    # Application name:
    name="dxlepoclient",

    # Version number:
    version=VERSION,

    # Requirements
    install_requires={
        "dxlclient",
    },

    # Application author details:
    author="McAfee, Inc.",

    # License
    license="Apache License 2.0",

    keywords=['opendxl', 'dxl', 'mcafee', 'client', 'epo'],

    # Packages
    packages=[
        "dxlepoclient",
    ],

    # Details
    url="http://www.mcafee.com/",

    description="McAfee ePolicy Orchestrator (ePO) DXL Python Client Library",

    long_description=open('README').read(),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
)
