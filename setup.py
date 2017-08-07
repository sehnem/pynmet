from setuptools import setup, find_packages

classifiers = ['Development Status :: 2 - Pre-Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: Python Software Foundation License',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name = 'pynmet',
      version = '0.1.2',
      author = 'Josué M. Sehnem',
      author_email = 'josue@sehnem.com',
      description = 'Python code to retrieve and plot inmet meteorological data',
      license = 'GPL',
      classifiers = classifiers,
      url = 'https://github.com/sehnem/pynmet/',
      download_url = 'https://github.com/sehnem/pynmet/archive/0.1.tar.gz',
      dependency_links = [],
      install_requires = ['pandas', 'bs4'],
      packages = find_packages(),
      include_package_data=True,
      package_data={'data':['data/estacoes.csv']}
      zip_safe=False)