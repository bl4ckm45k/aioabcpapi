from .admin import AdminApi
from .client import ClientApi
from ..base import BaseAbcp


class CpApi:
    def __init__(self, base: BaseAbcp):
        """
        :param base: BaseAbcp class object
        """
        self._base = base
        self.client = ClientApi(base)
        self.admin = AdminApi(base)
