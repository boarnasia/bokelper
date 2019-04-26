#!/usr/bin/env python
import os
import re
from setuptools import setup, find_packages


long_description = '(empty)'

try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        long_description = f.read()
except:  # noqa
    pass


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    path = os.path.join(os.path.dirname(__file__), package, '__init__.py')
    with open(path, 'rb') as f:
        init_py = f.read().decode('utf-8')
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name='bokelper',
    author='Boanasia',
    version=get_version('bokelper'),
    license='MIT',
    description='bokelper',
    long_description=long_description,
    packages=find_packages('.'),
    install_requires=[
        'bokeh~=1.1.0'
    ],
    extras_require={
        'test': [
            'pytest~=4.4.0',
            'pytest-cov~=2.6.1',
            'pytest-mypy~=0.3.2',
            'pytest-flake8~=1.0.4',
        ]
    },
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        # 'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        # 'Topic :: Software Development',
    ],
)
