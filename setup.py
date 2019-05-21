from setuptools import setup, find_packages
import versioneer

ver = versioneer.get_version()

classifiers = ['Development Status :: 2 - Pre-Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: Python Software Foundation License',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name = 'pynmet',
      version = ver,
      author = 'Josué M. Sehnem',
      author_email = 'josue@sehnem.com',
      description = 'Python code to retrieve and plot inmet meteorological data',
      license = 'GPLv3',
      classifiers = classifiers,
      url = 'https://gitlab.com/sehnem/pynmet/',
      download_url = 'https://gitlab.com/sehnem/pynmet/-/archive/{}/pynmet-{}.tar.gz'.format(ver, ver),
      dependency_links = [],
      install_requires = ['pandas', 'bs4', 'sqlalchemy', 'lxml', 'requests'],
      packages = find_packages(),
      include_package_data=True,
      cmdclass=versioneer.get_cmdclass(),
      zip_safe=False)
