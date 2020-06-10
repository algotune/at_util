#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['mysqlclient>=1.4.6',
                'pandas>=1.0.0',
                'SQLAlchemy>=1.3.17',
                'pyarrow>=0.17.1'
                ]
setup_requirements = ['pytest-runner']

test_requirements = ['pytest>=3']

setup(
    author="Bin Yang",
    author_email='bin.yang@algotune.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="at_util",
    install_requires=requirements,
    include_package_data=True,
    keywords='at_util',
    name='at_util',
    packages=find_packages(include=['at_util', 'at_util.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/algotune/at_util',
    version='0.0.1',
    zip_safe=False,
)
