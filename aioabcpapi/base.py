import asyncio
import logging
import ssl
import typing
from typing import Dict, List, Optional, Union, Type

import aiohttp
import certifi
import ujson as json
from aiohttp import FormData

from . import api
from .exceptions import NotEnoughRights
from .api import Headers, Methods

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('base')


class BaseAbcp:

    def __init__(
            self,
            host: str = None,
            login: str = None,
            password: str = None,
            loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None,
            connections_limit: int = None,
            timeout: typing.Optional[typing.Union[int, float, aiohttp.ClientTimeout]] = None,
    ):
        """ You can get API host name, login, password here: https://cp.abcp.ru/?page=allsettings&systemsettings&apiInformation

        :param host: host name from ABCP
        :type host: 'str'
        :param login: login from ABCP
        :type login: 'str'
        :param password: password from ABCP
        :type password: 'str' (md5 hash)
        :raise: when host, login or password is invalid
        """

        self._main_loop = loop
        # Authentication

        self._host = host
        self._login = login
        self._password = password
        self._admin = api.check_data(host, login, password)

        self._shipment_address = None
        self._shipment_method = None
        self._payment_method = None
        self._shipment_office = None
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())

        self._session: Optional[aiohttp.ClientSession] = None
        self._connector_class: Type[aiohttp.TCPConnector] = aiohttp.TCPConnector
        self._connector_init = dict(limit=connections_limit, ssl=self._ssl_context)
        self._headers = Headers()

        self.timeout = timeout

    async def _get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            connector=self._connector_class(**self._connector_init),
            json_serialize=json.dumps
        )

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
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

    def __payload_check(self, payload):
        if isinstance(payload, dict):
            payload['userlogin'] = self._login
            payload['userpsw'] = self._password
        elif isinstance(payload, FormData):
            payload.add_field('userlogin', self._login)
            payload.add_field('userpsw', self._password)
        if payload is None:
            payload = {'userlogin': self._login, 'userpsw': self._password}
        return payload

    async def _request(self, method: str,
                       payload: Union[Dict, FormData] = None, post: bool = False, **kwargs) -> Union[List, Dict, bool]:
        """
        Make an _request to ABCP API

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
        if not self._admin and (isinstance(method, Methods.Admin) or isinstance(method, Methods.TsAdmin)):
            raise NotEnoughRights('Недостаточно прав для использования API администратора')
        payload = self.__payload_check(payload)
        if isinstance(payload, FormData):
            headers = self._headers.multipart_header()
        elif method is Methods.Client.Search.ADVICES_BATCH:
            headers = self._headers.json_header()
            return await api.make_request_json(await self._get_session(), self._host, method, payload, headers)
        else:
            headers = self._headers.url_encoded_header()
        return await api.make_request(await self._get_session(), self._host,
                                      method, payload, headers, post, timeout=self.timeout, **kwargs)
