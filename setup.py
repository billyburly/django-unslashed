import os
from setuptools import setup
from unslashed import __version__
import pypandoc

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
long_description = pypandoc.convert('README.md', 'rst')

setup(
    name='tocka-django-unslashed',

    # Versions should comply with PEP440. For single-sourced versioning, see
    # https://packaging.python.org/en/latest/development.html#single-sourcing-the-version
    version=__version__,

    description='Django Middleware that can automatically remove trailing URL slashes and 301 redirect to the non-slash-terminated URL.',
    long_description=long_description,

    # The project URL
    url = 'https://github.com/frnhr/django-unslashed',

    # Author details
    author='Fran Hrzenjak',
    author_email='fran.hrzenjak@gmail.com',

    # Choose your license
    license='MIT License',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        # Extras
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP'],

    # What does your project relate to?
    keywords='django slash remove trailing unslash remove_slash path',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['unslashed'],

    # Run-time package dependencies. These will be installed by pip when your
    # project is installed.
    install_requires=['Django>=1.8'],

    # MANIFEST.in included entries should be included as package data and
    # installed into site-packages 
    include_package_data=True,

    # Default to False unless you specifically intend the package to be
    # installed as an .egg
    zip_safe=False,
)