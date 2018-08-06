from .inmet import sites, inmet
from .getdata import update_all

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
