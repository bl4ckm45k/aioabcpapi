from .admin import AdminApi
from .client import ClientApi
from ..base import BaseAbcp
from ..exceptions import AbcpWrongParameterError


class CpApi:
    """
    Базовый класс для CP API ABCP
    
    Предоставляет доступ к API для клиентов и администраторов.
    """

    def __init__(self, base: BaseAbcp):
        """
        Инициализация API CP ABCP
        
        :param base: Объект с базовой конфигурацией API
        :type base: BaseAbcp
        """
        if not isinstance(base, BaseAbcp):
            raise AbcpWrongParameterError("base", base, "BaseAbcp instance")

        self._base = base
        self._client = None
        self._admin = None

    @property
    def client(self) -> 'ClientApi':
        """
        Получить доступ к API клиента
        
        :return: Объект с API для клиента
        :rtype: ClientApi
        """
        if self._client is None:
            self._client = ClientApi(self._base)
        return self._client

    @property
    def admin(self) -> 'AdminApi':
        """
        Получить доступ к API администратора
        
        :return: Объект с API для администратора
        :rtype: AdminApi
        """
        if self._admin is None:
            self._admin = AdminApi(self._base)
        return self._admin
