#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='django-fflag',
    version='0.1.0',
    url='',
    description='Feature flag for django',
    keywords=['feature-flag'],
    long_description='',
    author='Vladislav Bakin',
    author_email='vladislav@bakin.me',
    maintainer='Vladislav Bakin',
    maintainer_email='vladislav@bakin.me',

    license='MIT',

    install_requires=[],
    tests_require=['pytest'],

    packages=find_packages(exclude=['tests.*', 'tests']),

    test_suite='tests',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
