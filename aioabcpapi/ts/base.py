from typing import Optional

from .admin import TsAdminApi
from .client import TsClientApi
from ..base import BaseAbcp


class TsApi:
    def __init__(self, base: BaseAbcp):
        """
        :param base: BaseAbcp class object
        """
        if not isinstance(base, BaseAbcp):
            raise TypeError("Expected a BaseAbcp instance")
        self._base = base
        self._client: Optional[TsClientApi] = None
        self._admin: Optional[TsAdminApi] = None

    @property
    def client(self) -> TsClientApi:
        if self._client is None:
            self._client = TsClientApi(self._base)
        return self._client

    @property
    def admin(self) -> TsAdminApi:
        if self._admin is None:
            self._admin = TsAdminApi(self._base)
        return self._admin
