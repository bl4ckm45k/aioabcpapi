from .admin import TsAdminApi
from .client import TsClientApi
from ..base import BaseAbcp


class TsApi:
    def __init__(self, base: BaseAbcp):
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
        self.client = TsClientApi(base)
        self.admin = TsAdminApi(base)
