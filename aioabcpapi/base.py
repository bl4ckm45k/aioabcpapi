import asyncio
import logging
import ssl
from typing import Dict, List, Optional, Union, Type, Any

import aiohttp
import certifi
import ujson
from aiohttp import FormData

from .api import Headers, _Methods, check_data, make_request_json, make_request
from .exceptions import NotEnoughRights

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('base')


class BaseAbcp:

    def __init__(
            self,
            host: str,
            login: str,
            password: str,
            loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None,
            connections_limit: int = None,
            timeout: Optional[Union[int, float, aiohttp.ClientTimeout]] = None,
    ):
        """Для получения доступа к API если вы являетесь администратором, перейдите в ПУ.

        https://cp.abcp.ru/?page=allsettings&systemsettings&apiInformation

        Если вы являетесь клиентом, запросите доступ у вашего менеджера.

        :param host: Хост
        :param login: Логин
        :param password: MD5-пароль
        :raise: when host, login or password is invalid
        :return: Объект класса
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

        self.timeout = timeout

    async def _get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            connector=self._connector_class(**self._connector_init),
            json_serialize=ujson.dumps
        )

    @property
    def _loop(self) -> Optional[asyncio.AbstractEventLoop]:
        return self._main_loop

    async def _get_session(self) -> Optional[aiohttp.ClientSession]:
        if self._session is None or self._session.closed:
            self._session = await self._get_new_session()

        if not self._session._loop.is_running():
            await self._session.close()
            self._session = await self._get_new_session()

        return self._session

    async def close(self):
        """
        Close all client sessions
        """
        if self._session:
            await self._session.close()

    def __payload_check(self, payload: Union[Dict[str, Any], FormData]) -> Union[Dict[str, Any], FormData]:
        if isinstance(payload, dict):
            payload['userlogin'] = self._login
            payload['userpsw'] = self._password
            return payload
        elif isinstance(payload, FormData):
            payload.add_field('userlogin', self._login)
            payload.add_field('userpsw', self._password)
            return payload
        elif payload is None:
            payload = {'userlogin': self._login, 'userpsw': self._password}
        return payload

    async def request(self, method: str,
                      payload: Union[Dict[str, Any], FormData] = None,
                      post: bool = False, **kwargs) -> Union[List, Dict, bool]:
        """
        Make an request to ABCP API

        https://www.abcp.ru/wiki/API:Docs

        :param method: API method
        :type method: :obj:`str`
        :param payload: _request parameters
        :type payload: :obj:`dict`
        :param post:
        :return: result
        :rtype: Union[List, Dict]
        :raise: :obj:`utils.exceptions`
        """
        if not self.admin and isinstance(method, (_Methods.Admin, _Methods.TsAdmin)):
            raise NotEnoughRights('Недостаточно прав для использования API администратора')
        payload = self.__payload_check(payload)
        if isinstance(payload, FormData):
            headers = self._headers.multipart_header()
        elif kwargs is not None and 'json' in kwargs.keys():
            headers = self._headers.json_header()
            return await make_request_json(await self._get_session(), self._host, method, payload, headers)
        else:
            headers = self._headers.url_encoded_header()
        return await make_request(await self._get_session(), self._host,
                                  method, payload, headers, post, timeout=self.timeout, **kwargs)
