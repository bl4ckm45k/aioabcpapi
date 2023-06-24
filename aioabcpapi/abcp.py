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
        self.cp = CpApi(self._base)
        self.ts = TsApi(self._base)
