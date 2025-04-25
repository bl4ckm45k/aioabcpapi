from typing import Optional, AsyncContextManager

from .base import BaseAbcp
from .cp.base import CpApi
from .ts.base import TsApi


class Abcp(AsyncContextManager):
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
        """
        Получить экземпляр CP API

        :return: Экземпляр CpApi
        """
        if self._cp is None:
            self._cp = CpApi(self._base)
        return self._cp

    @property
    def ts(self) -> TsApi:
        """
        Получить экземпляр TS API

        :return: Экземпляр TsApi
        """
        if self._ts is None:
            self._ts = TsApi(self._base)
        return self._ts

    async def close(self) -> None:
        """
        Закрыть все сессии клиента
        
        :return: None
        """
        return await self._base.close()

    async def __aenter__(self) -> 'Abcp':
        """
        Асинхронный контекстный менеджер - вход
        
        :return: Экземпляр Abcp
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Асинхронный контекстный менеджер - выход
        Закрывает все сессии
        
        :return: None
        """
        await self.close()
