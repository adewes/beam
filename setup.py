from distutils.core import setup
from setuptools import find_packages

setup(
    name='beam',
    python_requires='>=3',
    version='0.11',
    author='Andreas Dewes - 7scientists',
    author_email='andreas@7scientists.com',
    license='MIT',
    url='https://github.com/adewes/beam',
    packages=find_packages(),
    package_data={'': ['*.ini']},
    include_package_data=True,
    install_requires=['click', 'pyyaml', 'markdown2', 'jinja2'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'beam = beam.cli.main:beam'
        ]
    },
    description='A simple yet powerful static site generator aimed at product pages (not blogs).',
    long_description="""A simple yet powerful static site generator for Python.

Templates (HTML, Markdown, ...) go in, pages come out.
"""
)