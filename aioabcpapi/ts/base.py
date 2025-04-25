from .admin import TsAdminApi
from .client import TsClientApi
from ..base import BaseAbcp
from ..exceptions import AbcpWrongParameterError


class TsApi:
    """
    Базовый класс для TS API ABCP (API 2.0)
    
    Предоставляет доступ к API 2.0 для клиентов и администраторов.
    """

    def __init__(self, base: BaseAbcp):
        """
        Инициализация API TS ABCP
        
        :param base: Объект с базовой конфигурацией API
        :type base: BaseAbcp
        """
        if not isinstance(base, BaseAbcp):
            raise AbcpWrongParameterError("base", base, "BaseAbcp instance")
        self._base = base
        self._client = None
        self._admin = None

    @property
    def client(self) -> 'TsClientApi':
        """
        Получить доступ к API клиента
        
        :return: Объект с API для клиента
        :rtype: ClientApi
        """
        if self._client is None:
            from .client import TsClientApi
            self._client = TsClientApi(self._base)
        return self._client

    @property
    def admin(self) -> 'TsAdminApi':
        """
        Получить доступ к API администратора
        
        :return: Объект с API для администратора
        :rtype: AdminApi
        """
        if self._admin is None:
            from .admin import TsAdminApi
            self._admin = TsAdminApi(self._base)
        return self._admin
