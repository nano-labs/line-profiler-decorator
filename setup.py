"""

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='line-profiler-decorator',

    version='0.0.5',

    description='Line profiler Output time usage per line',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://github.com/nano-labs/line-profiler-decorator',
    download_url='https://github.com/nano-labs/line-profiler-decorator/archive/refs/tags/0.0.5.zip',

    # Author details
    author='Fabio Pachelli Pacheco',
    author_email='nanook.labs@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='line time profiler decorator',

    packages=['line_profiler_decorator'],
    scripts=[],

    install_requires=["line-profiler==3.3.0",],
    python_requires='>3.6.0'
)
