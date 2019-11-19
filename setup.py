# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyrduino',
    author='Ahti Komu',
    author_email='ahti.komu@gmail.com',
    description='More object oriented wrapper on top of pyfirmata package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'pyfirmata',
        'dotmap',
        'pyserial',
    ],
    keywords='arduino',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    version='1.0',
    # py_modules=['pyrduino'],
    python_requires='>=3',
    entry_points='''
         [console_scripts]
         pyrduino_example=example:cli
     ''',
)