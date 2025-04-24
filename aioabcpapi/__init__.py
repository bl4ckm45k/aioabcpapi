import sys

from .abcp import Abcp
from .base import BaseAbcp
from .exceptions import (NetworkError, UnsupportedHost, UnsupportedLogin, PasswordType, NotEnoughRights, AbcpAPIError,
                         AbcpParameterRequired, TeaPot, AbcpNotFoundError, FileSizeExceeded, AbcpWrongParameterError)

if sys.version_info < (3, 10):
    raise RuntimeError('Your Python version {0} is not supported, please install '
                       'Python 3.10+'.format('.'.join(map(str, sys.version_info[:3]))))

__author__ = 'bl4ckm45k'
__version__ = '2.2.0'
__email__ = 'nonpowa@gmail.com'

__all__ = [
    'BaseAbcp',
    'Abcp',
    'NetworkError',
    'UnsupportedHost',
    'UnsupportedLogin',
    'PasswordType',
    'NotEnoughRights',
    'AbcpAPIError',
    'AbcpParameterRequired',
    'TeaPot',
    'AbcpNotFoundError',
    'FileSizeExceeded',
    'AbcpWrongParameterError'
]
