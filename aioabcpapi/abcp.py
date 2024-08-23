from typing import Optional

from aioabcpapi import BaseAbcp
from aioabcpapi.cp.base import CpApi
from aioabcpapi.ts.base import TsApi


class Abcp:
    def __init__(self, host: str, login: str, password: str):
        """
        Инициализация класса API

        api = Abcp(host, login, password)

        Доступные методы:

        cp - API ABCP

        ts - API TS (API 2.0)

        :param host: Хост
        :param login: Логин
        :param password: MD5-пароль
        """
        self._base = BaseAbcp(host, login, password)
        self._cp: Optional[CpApi] = None
        self._ts: Optional[TsApi] = None

    @property
    def cp(self) -> CpApi:
        if self._cp is None:
            self._cp = CpApi(self._base)
        return self._cp

    @property
    def ts(self) -> TsApi:
        if self._ts is None:
            self._ts = TsApi(self._base)
        return self._ts

    async def close(self):
        return await self._base.close()
