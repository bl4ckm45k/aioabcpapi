import sys

if sys.version_info < (3, 7):
    raise ImportError('Your Python version {0} is not supported, please install '
                      'Python 3.7+'.format('.'.join(map(str, sys.version_info[:3]))))

from .abcp import AbcpApi
from .api import check_result, make_request, Methods
from .exceptions import (NetworkError, UnsupportedHost, UnsupportedLogin, PasswordType, NotEnoughRights, AbcpAPIError,
                         AbcpParameterRequired, TeaPot)

__author__ = 'bl4ckm45k'
__version__ = '0.4.2'
__email__ = 'nonpowa@gmail.com'
