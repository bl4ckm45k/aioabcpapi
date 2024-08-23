from typing import Optional

from .admin import AdminApi
from .client import ClientApi
from ..base import BaseAbcp


class CpApi:
    def __init__(self, base: BaseAbcp):
        """
        :param base: BaseAbcp class object
        """
        if not isinstance(base, BaseAbcp):
            raise TypeError("Expected a BaseAbcp instance")

        self._base = base
        self._client: Optional[ClientApi] = None
        self._admin: Optional[AdminApi] = None

    @property
    def client(self) -> ClientApi:
        if self._client is None:
            self._client = ClientApi(self._base)
        return self._client

    @property
    def admin(self) -> AdminApi:
        if self._admin is None:
            self._admin = AdminApi(self._base)
        return self._admin
