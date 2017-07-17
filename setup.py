from setuptools import setup, find_packages

classifiers = ['Development Status :: 1 - Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name              = 'pynmet',
      version           = '0.1',
      author            = 'Josué M. Sehnem',
      author_email      = 'josue@sehnem.com',
      description       = 'Python code to retrieve and plot inmet meteorological data',
      license           = 'GPL',
      classifiers       = classifiers,
      url               = 'https://github.com/sehnem/pynmet/',
      dependency_links  = [],
      install_requires  = [],
      packages          = find_packages())