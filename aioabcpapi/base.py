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
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        self._session: Optional[aiohttp.ClientSession] = None
        self._connector_class: Type[aiohttp.TCPConnector] = aiohttp.TCPConnector
        self._connector_init = dict(limit=connections_limit, ssl=ssl_context)

        self._timeout = None
        self.timeout = timeout

    async def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            connector=self._connector_class(**self._connector_init),
            json_serialize=json.dumps
        )

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
        return self._main_loop

    async def get_session(self) -> Optional[aiohttp.ClientSession]:
        if self._session is None or self._session.closed:
            self._session = await self.get_new_session()

        if not self._session._loop.is_running():
            await self._session.close()
            self._session = await self.get_new_session()

        return self._session

    def session(self) -> Optional[aiohttp.ClientSession]:
        return self._session

    async def close(self):
        """
        Close all client sessions
        """
        if self._session:
            await self._session.close()

    async def request(self, method: str,
                      data: Union[Dict, FormData] = None, post: bool = False, **kwargs) -> Union[List, Dict, bool]:
        """
        Make an request to ABCP API

        https://www.abcp.ru/wiki/API:Docs

        :param method: API method
        :type method: :obj:`str`
        :param data: request parameters
        :param post:
        :type data: :obj:`dict`
        :return: result
        :rtype: Union[List, Dict]
        :raise: :obj:`utils.exceptions`
        """
        if isinstance(data, dict):
            data['userlogin'] = self._login
            data['userpsw'] = self._password
        elif isinstance(data, FormData):
            data.add_field('userlogin', self._login)
            data.add_field('userpsw', self._password)
        if data is None:
            data = {'userlogin': self._login, 'userpsw': self._password}

        return await api.make_request(await self.get_session(), self._host, self._admin,
                                      method, data, post, timeout=self.timeout, **kwargs)
