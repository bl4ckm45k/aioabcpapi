from .admin import TsAdminApi
from .client import TsClientApi
from ..base import BaseAbcp


class TsApi(BaseAbcp):
    def __init__(self, *args):
        super().__init__(*args)
        # If you know how do it other way please commit on https://github.com/bl4ckm45k/aioabcpapi
        self.client = TsClientApi(*args)
        self.admin = TsAdminApi(*args)
