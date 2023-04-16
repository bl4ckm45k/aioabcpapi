import sys
from .base import BaseAbcp
from .abcp import Abcp
from .api import check_result, make_request, Methods
from .exceptions import (NetworkError, UnsupportedHost, UnsupportedLogin, PasswordType, NotEnoughRights, AbcpAPIError,
                         AbcpParameterRequired, TeaPot)

if sys.version_info < (3, 7):
    raise RuntimeError('Your Python version {0} is not supported, please install '
                       'Python 3.7+'.format('.'.join(map(str, sys.version_info[:3]))))

__author__ = 'bl4ckm45k'
__version__ = '1.1.4'
__email__ = 'nonpowa@gmail.com'
