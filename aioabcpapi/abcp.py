from aioabcpapi import BaseAbcp
from aioabcpapi.cp.base import CpApi
from aioabcpapi.ts.base import TsApi


class Abcp(BaseAbcp):
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
        super().__init__(host, login, password)
        self.cp = CpApi(host, login, password)
        self.ts = TsApi(host, login, password)
