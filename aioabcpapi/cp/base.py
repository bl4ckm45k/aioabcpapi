from .admin import AdminApi
from .client import ClientApi
from ..base import BaseAbcp


class CpApi(BaseAbcp):
    def __init__(self,  host: str, login: str, password: str):
        """
        Класс для доступа к методам API ABCP

        client - Общий интерфейс

        https://www.abcp.ru/wiki/API.ABCP.Client

        admin - Административный интерфейс

        https://www.abcp.ru/wiki/API.ABCP.Admin
        """
        super().__init__(host, login, password)
        self.client = ClientApi(host, login, password)
        self.admin = AdminApi(host, login, password)
