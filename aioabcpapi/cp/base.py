from .admin import AdminApi
from .client import ClientApi
from ..base import BaseAbcp


class CpApi(BaseAbcp):
    def __init__(self, *args):
        super().__init__(*args)
        # If you know how do it other way please commit on https://github.com/bl4ckm45k/aioabcpapi
        self.client = ClientApi(*args)
        self.admin = AdminApi(*args)
