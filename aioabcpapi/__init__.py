import sys
from .base import BaseAbcp
from .abcp import Abcp
from .exceptions import (NetworkError, UnsupportedHost, UnsupportedLogin, PasswordType, NotEnoughRights, AbcpAPIError,
                         AbcpParameterRequired, TeaPot)

if sys.version_info < (3, 8):
    raise RuntimeError('Your Python version {0} is not supported, please install '
                       'Python 3.8+'.format('.'.join(map(str, sys.version_info[:3]))))

__author__ = 'bl4ckm45k'
__version__ = '2.0.7'
__email__ = 'nonpowa@gmail.com'
