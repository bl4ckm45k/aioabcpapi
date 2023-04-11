from .admin import TsAdminApi
from .client import TsClientApi
from ..base import BaseAbcp


class TsApi(BaseAbcp):
    def __init__(self,  host: str, login: str, password: str):
        """
        Класс для доступа к методам API ABCP 2.0 (TS)

        client - Общий интерфейс

        https://www.abcp.ru/wiki/API.ABCP.Client

        admin - Административный интерфейс

        https://www.abcp.ru/wiki/API.ABCP.Admin
        :param host: Хост
        :param login: Логин
        :param password: MD5-пароль
        """
        super().__init__(host, login, password)
        self.client = TsClientApi(host, login, password)
        self.admin = TsAdminApi(host, login, password)
