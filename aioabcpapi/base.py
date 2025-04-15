import asyncio
import logging
import ssl
from types import TracebackType
from typing import Dict, List, Optional, Union, Type, Any, TypeVar

import aiohttp
import certifi
import ujson
from aiohttp import FormData, ClientTimeout

from .api import Headers, _Methods, check_data, make_request
from .exceptions import NotEnoughRights, AbcpBaseException

logger = logging.getLogger('aioabcpapi.base')

T = TypeVar('T', bound='BaseAbcp')


class BaseAbcp:
    """Базовый класс для работы с API ABCP"""

    def __init__(
            self,
            host: str,
            login: str,
            password: str,
            loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None,
            connections_limit: int | None = None,
            timeout: Optional[Union[int, float, aiohttp.ClientTimeout]] = None,
            retry_attempts: int = 3,
            retry_delay: float = 0.3,
    ):
        """Для получения доступа к API если вы являетесь администратором, перейдите в ПУ.

        https://cp.abcp.ru/?page=allsettings&systemsettings&apiInformation

        Если вы являетесь клиентом, запросите доступ у вашего менеджера.

        :param host: Хост
        :param login: Логин
        :param password: MD5-пароль
        :param loop: Опциональный event loop для асинхронных операций
        :param connections_limit: Лимит одновременных соединений
        :param timeout: Таймаут запросов (в секундах или объект aiohttp.ClientTimeout)
        :param retry_attempts: Количество попыток повтора при сетевых ошибках
        :param retry_delay: Задержка между попытками повтора (в секундах)
        :raise: UnsupportedHost, UnsupportedLogin, PasswordType - когда хост, логин или пароль некорректны
        :return: Объект класса BaseAbcp
        """

        self._main_loop = loop
        # Authentication
        self._host = host
        self._login = login
        self._password = password
        self.admin = check_data(host, login, password)

        self.shipment_address = None
        self.shipment_method = None
        self.payment_method = None
        self.shipment_office = None
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())

        self._session: Optional[aiohttp.ClientSession] = None
        self._connector_class: Type[aiohttp.TCPConnector] = aiohttp.TCPConnector
        self._connector_init = dict(limit=connections_limit, ssl=self._ssl_context)
        self._headers = Headers()

        # Настройка таймаута
        if isinstance(timeout, (int, float)):
            self.timeout = ClientTimeout(total=timeout)
        else:
            self.timeout = timeout
            
        # Настройка ретраев
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay

    async def _get_new_session(self) -> aiohttp.ClientSession:
        """
        Создает новую клиентскую сессию
        
        :return: Новая aiohttp.ClientSession
        """
        return aiohttp.ClientSession(
            connector=self._connector_class(**self._connector_init),
            json_serialize=ujson.dumps,
            timeout=self.timeout
        )

    @property
    def _loop(self) -> Optional[asyncio.AbstractEventLoop]:
        """
        Получает текущий event loop
        
        :return: Event loop
        """
        if self._main_loop is None:
            try:
                return asyncio.get_running_loop()
            except RuntimeError:
                return None
        return self._main_loop

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Получает текущую сессию или создает новую
        
        :return: Активная aiohttp.ClientSession
        """
        if self._session is None or self._session.closed:
            self._session = await self._get_new_session()
        
        loop = getattr(self._session, "_loop", None)
        if loop and not loop.is_running():
            await self._session.close()
            self._session = await self._get_new_session()
            
        return self._session

    async def close(self) -> None:
        """
        Закрывает все клиентские сессии
        
        :return: None
        """
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self: T) -> T:
        """
        Входная точка асинхронного контекстного менеджера
        
        :return: self
        """
        return self
        
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        """
        Выходная точка асинхронного контекстного менеджера
        
        :return: None
        """
        await self.close()

    def __payload_check(self, payload: Optional[Union[Dict[str, Any], FormData]]) -> Union[Dict[str, Any], FormData]:
        """
        Проверяет и дополняет payload учетными данными
        
        :param payload: Исходный payload
        :return: Дополненный payload
        """
        if isinstance(payload, dict):
            payload = payload.copy()  # Создаем копию, чтобы не модифицировать оригинал
            payload['userlogin'] = self._login
            payload['userpsw'] = self._password
            return payload
        elif isinstance(payload, FormData):
            # FormData не поддерживает копирование, поэтому добавляем поля к оригиналу
            payload.add_field('userlogin', self._login)
            payload.add_field('userpsw', self._password)
            return payload
        else:
            # None или другой неподдерживаемый тип
            return {'userlogin': self._login, 'userpsw': self._password}

    async def request(
        self, 
        method: str,
        payload: Optional[Union[Dict[str, Any], FormData]] = None,
        post: bool = False, 
        retry: int | None = None,
        **kwargs
    ) -> Union[List, Dict, bool]:
        """
        Выполняет запрос к API ABCP с автоматическими повторными попытками при сетевых ошибках.

        https://www.abcp.ru/wiki/API:Docs

        :param method: Метод API
        :type method: :obj:`str`
        :param payload: Параметры запроса
        :type payload: :obj:`dict` или FormData
        :param post: Использовать ли метод POST вместо GET
        :param retry: Количество повторных попыток (если не указано, используется self.retry_attempts)
        :param kwargs: Дополнительные параметры для передачи в aiohttp.request
        :return: Результат запроса
        :rtype: Union[List, Dict, bool]
        :raises: :obj:`exceptions.AbcpBaseException` и его подклассы
        """
        if not self.admin and isinstance(method, (_Methods.Admin, _Methods.TsAdmin)):
            raise NotEnoughRights('Недостаточно прав для использования API администратора')
            
        attempts = retry if retry is not None else self.retry_attempts
        last_exception = None
        
        for attempt in range(1, attempts + 1):
            try:
                checked_payload = self.__payload_check(payload)
                http_method = "POST" if post else "GET"
                
                # Определение заголовков на основе типа данных и параметров
                if isinstance(checked_payload, FormData):
                    headers = self._headers.multipart_header()
                elif kwargs is not None and 'json' in kwargs:
                    headers = self._headers.json_header()
                else:
                    headers = self._headers.url_encoded_header()
                
                # Используем универсальную функцию make_request
                return await make_request(
                    await self._get_session(), 
                    self._host,
                    method, 
                    checked_payload, 
                    headers, 
                    http_method=http_method,
                    timeout=self.timeout, 
                    **kwargs
                )
            except AbcpBaseException as e:
                # Не повторяем запрос при ошибках бизнес-логики или авторизации
                if not isinstance(e, (NotEnoughRights)):
                    raise
                last_exception = e
                raise
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_exception = e
                logger.warning(
                    f"Attempt {attempt}/{attempts} failed with error: {e.__class__.__name__}: {e}"
                )
                
                if attempt < attempts:
                    await asyncio.sleep(self.retry_delay * attempt)  # Увеличиваем задержку с каждой попыткой
                else:
                    # Все попытки исчерпаны
                    from .exceptions import NetworkError
                    raise NetworkError(f"All {attempts} attempts failed. Last error: {e.__class__.__name__}: {e}")
        
        # Этот код не должен выполняться, но добавлен для типизации
        from .exceptions import NetworkError
        raise NetworkError(f"Unexpected error during request execution: {last_exception}")
