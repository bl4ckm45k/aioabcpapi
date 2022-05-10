import asyncio
from datetime import datetime
import logging
import ssl
import typing
from typing import Dict, List, Optional, Union, Type

import aiohttp
import certifi
import ujson as json

from . import api
from .exceptions import NotEnoughRights, AbcpAPIError, AbcpParameterRequired
from .payload import generate_payload, generate_payload_filter, generate_payload_payments, \
    generate_payload_online_order

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('abcp')


class AbcpApi:

    def __init__(
            self,
            host: str = None,
            login: str = None,
            password: str = None,
            loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None,
            connections_limit: int = None,
            validate: bool = True,
            timeout: typing.Optional[typing.Union[int, float, aiohttp.ClientTimeout]] = None,
    ):
        """ You can get API host name, login, password here: https://cp.abcp.ru/?page=support

        :param host: host name from ABCP
        :type host: 'str'
        :param login: login from ABCP
        :type login: 'str'
        :param password: password from ABCP
        :type password: 'str' (md5 hash)
        :param validate: Validate host, login, password
        :type validate: bool
        :param admin: Can use Api.Admin or not
        :type admin: bool
        :raise: when host, login or password is invalid
        """

        self._main_loop = loop

        # Authentication
        if validate:
            valid, admin = api.check_data(host, login, password)
            self._admin = admin
        self._host = host
        self._login = login
        self._password = password

        self._shipment_address = None
        self._shipment_method = None
        self._payment_method = None
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
                      data: Optional[Dict] = None, post: bool = False, **kwargs) -> Union[List, Dict, bool]:
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

        return await api.make_request(await self.get_session(), self._host, self._login, self._password, self._admin,
                                      method, data, post, timeout=self.timeout, **kwargs)

    async def get_orders_list(
            self,
            date_created_start: str = None,
            date_created_end: str = None,
            date_updated_start: str = None,
            date_updated_end: str = None,
            numbers: Union[str, int, List] = None,
            internal_numbers: Optional[List] = None,
            status_code: Union[str, int, List] = None,
            office_id: Union[int, str] = None,
            distributor_order_id: Union[int, str] = None,
            is_canceled: Union[int, str] = None,
            distributor_id: Union[str, int, List] = None,
            with_deleted: Optional[str] = None,
            format: Optional[str] = None,
            limit: Optional[int] = None,
            skip: Optional[int] = None,
            desc: str = 'false'

    ):
        """Принимает в качестве параметров условия фильтрации заказов. Возвращает список заказов (в т.ч. список позиций заказа).

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.BE.D0.B2

        :param date_created_start: Начальная дата размещения заказа<br><br>
        :type date_created_start: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")<br><br>
        :param date_created_end: Конечная дата размещения заказа<br><br>
        :type date_created_end: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        :param date_updated_start: Начальная дата последнего обновления заказа в формате<br><br>
        :type date_updated_start: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        :param date_updated_end: Конечная дата последнего обновления заказа в формате<br><br>
        :type date_updated_end:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        :param numbers: Массив номеров заказов<br><br>
        :type numbers: list
        :param internal_numbers: Массив номеров заказов в учетной системе (например, в 1С). Используется только, если в параметрах запроса не задан numbers.<br><br>
        :type internal_numbers: list
        :param status_code: Код статус позиции заказа (один или массив кодов). Будут выбраны заказы содержащие хотя бы одну позицию в данном статусе.<br><br>
        :type status_code: Union[str, int, list]
        :param office_id: Идентификатор офиса (в ответе по параметру могут быть отфильтрованы заказы где этот офис выбран как самовывоз или если это офис клиента или если менеджер клиента, сделавшего заказ, относится к данному офису)<br><br>
        :type office_id: int or str
        :param distributor_order_id: Идентификатор заказа у поставщика. В результате вернутся все заказы которые были отправлены поставщику под этим номером.<br><br>
        :type distributor_order_id: int or str
        :param is_canceled: Флаг "Запрос на удаление позиции". 0 - запрос не был отправлен, 1 - запрос отправлен, 2 - запрос отклонен менеджером.<br><br>
        :type is_canceled: int or str
        :param distributor_id: Идентификатор (один или массив идентификаторов) поставщика. В результате вернутся все заказы, содержащие хотя бы одну позицию от указанного поставщика.<br><br>
        :type distributor_id: Union[str, int, list]
        :param with_deleted: Признак, возвращать ли в ответе удаленные заказы и позиции <br><br>
        :type with_deleted: str or bool ('true', 'false', True, False)
        :param format: Формат ответа. Доступные значения <br>
               additional - дописывает к заказу данные клиента при гостевом заказе; к позициям добавляет значение vinQueryIds
               <br><br>short - сокращенный вариант отображения без содержимого позиций заказов
               <br><br>count - возвращает только количество заказов по заданным условиям
               <br><br>status_only - возвращает только номер заказа, а в узле позиций: id, statusCode, brand, number, numberFix, code
               <br><br>p - заказы содержатся в поле items, данные о количестве содержатся в поле count
        :type format: str
        :param limit: Ограничение на возвращаемое кол-во
        :type limit: int
        :param skip: Сколько заказов пропустить
        :type skip: int
        :param desc: Обратный порядок
        :type desc: : str or bool ('true', 'false', True, False)


        """
        if limit is not None and int(limit) <= 1:
            raise AbcpAPIError(f'The limit must be more than {limit}')
        if type(status_code) is not list and status_code is not None:
            status_code = [status_code]
        if type(numbers) is not list and numbers is not None:
            numbers = [numbers]
        payload = generate_payload(**locals())

        return await self.request(api.Methods.GET_ORDERS_LIST, payload)

    async def get_order(
            self,
            number: Union[int, str] = None,
            internal_number: Union[int, str] = None,
            with_deleted: str = None,
            format: str = None

    ):
        """Принимает в качестве параметра онлайн-номер заказа. Возвращает информацию о заказе (в т.ч. список позиций заказа).

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B8.D0.BD.D1.84.D0.BE.D1.80.D0.BC.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B5

        :param number: Номер заказа int или str
        :type number: int or str
        :param internal_number: Массив номеров заказов в учетной системе (например, в 1С).
                Используется только, если в параметрах запроса не задан numbers.
        :type internal_number: int or str
        :param with_deleted: Признак, возвращать ли в ответе удаленные заказы и позиции
        :type with_deleted: str or bool ('true', 'false', True, False)
        :param format: Формат ответа. Доступные значения
               additional - дописывает к заказу данные клиента при гостевом заказе; к позициям добавляет значение vinQueryIds
               short - сокращенный вариант отображения без содержимого позиций заказов
               count - возвращает только количество заказов по заданным условиям
               status_only - возвращает только номер заказа, а в узле позиций: id, statusCode, brand, number, numberFix, code
               p - заказы содержатся в поле items, данные о количестве содержатся в поле count
        :type format: str

        """
        if number is None and internal_number is None:
            raise AbcpParameterRequired(f'number and internal_number is None')
        payload = generate_payload(**locals())

        return await self.request(api.Methods.GET_ORDER, payload)

    async def status_history(
            self,
            position_id: Union[int, str]

    ):
        """Принимает в качестве параметра id позиции заказа. Возвращает информацию об истории изменений статуса позиции заказа.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B8.D1.81.D1.82.D0.BE.D1.80.D0.B8.D0.B8_.D0.B8.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B9_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0

        :param position_id: Номер заказа int или str<br><br>
        :type position_id int or str


        """
        payload = generate_payload(**locals())

        return await self.request(api.Methods.STATUS_HISTORY, payload)

    async def create_or_edit_order(
            self,
            number: Union[int, str] = None,
            internal_number: Union[int, str] = None,
            date: str = None,
            order_positions: Union[List[Dict], Dict] = None,
            user_id: Union[int, str] = None,
            delivery_type_id: Union[int, str] = None,
            delivery_office_id: Union[int, str] = None,
            basket_id: Union[int, str] = None,
            guest_order_name: str = None,
            guest_order_mobile: str = None,
            guest_order_email: str = None,
            shipment_date: str = None,
            delivery_cost: Union[str, int, float] = None,
            delivery_address_id: Union[int, str] = None,
            delivery_address: str = None,
            client_order_number: str = None,
            note: str = None,
            del_note: Union[str, int] = None

    ):
        """Универсальный метод сохранения. Принимает в качестве параметра объект описывающий заказ. Для создания заказа от имени Гостя, необходимо передавать корректно заполненные параметры: guestOrderName и guestOrderMobile или guestOrderEmail, в зависимости от обязательности полей "Мобильный" или "Email" в форме создания гостевого заказа.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.A1.D0.BE.D1.85.D1.80.D0.B0.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0
        :param date
        :param number: Онлайн-номер заказа
        :type number: int or str
        :param internal_number: Внутренний номер заказа, обязательный параметр для создания<br><br>
        :type internal_number int or str
        :param order_positions: Список словарей описывающих позиции, читайте документацию API.ABCP.Admin<br>В случае редактирования заказа, могут быть указаны только позиции и поля, которые требуют изменения. В случае создания заказа, должны быть указаны все позиции со всеми полями (кроме полей comment, supplierCode и itemKey). При редактировании позиций обязательна передача параметра id. Если параметр id не передан, будет добавлена новая позиция. При добавлении позиции все поля (кроме полей comment, supplierCode и itemKey) для нее являются обязательными. Для удаления позиции необходимо указать ей количество 0 или установить параметр delete в значение 1.<br><br>
        :type order_positions: list of dictionaries
        :param client_order_number: Номер заказа в системе учета клиента<br><br>
        :type client_order_number: int or str
        :param user_id: Идентификатор клиента на сайте, для которого создается заказ. Обязательный параметр, если создается заказ на клиента или сотрудника<br>
        :type user_id: int or str
        :param delivery_type_id: Тип доставки<br>
        :type delivery_type_id: int or str
        :param delivery_office_id: Идентификатор офиса самовывоза <br>
        :type delivery_office_id: int or str
        :param basket_id: 	Необязательный параметр - идентификатор корзины при использовании мультикорзины<br>
        :type basket_id: int or str
        :param guest_order_name: Необязательный параметр - имя клиента для оформления заказа от имени Гостя. Для корректного оформления заказа под гостем должны быть указаны параметры guestOrderName и guestOrderMobile или guestOrderEmail.
        :type guest_order_name: str
        :param guest_order_mobile: Необязательный параметр - контактный телефон клиента для оформления заказа от имени Гостя. (в формате 70000000000). Для корректного оформления заказа под гостем должны быть указаны параметры guestOrderName и guestOrderMobile или guestOrderEmail.
        :type guest_order_mobile: str
        :param guest_order_email: Необязательный параметр - e-mail для оформления заказа от имени Гостя. (в формате user@domain.com). Для корректного оформления заказа под гостем должны быть указаны параметры guestOrderName и guestOrderMobile или guestOrderEmail.
        :type guest_order_email: str
        :param shipment_date: Дата доставки
        :type shipment_date: datetime.datetime.now().strftime("%Y-%m-%d")
        :param delivery_cost: Цена доставки
        :type delivery_cost: int or float
        :param delivery_address_id: Число. Идентификатор адреса доставки. Если нужно создать новый адрес, то нужно передать "-1" и в параметре deliveryAddress новый адрес доставки.
        :type delivery_address_id: str or int
        :param delivery_address: Текст. Адрес доставки, в случае, когда необходимо сразу создать новый адрес нужно в deliveryAddressId передавать "-1" + адрес доставки
        :type delivery_address: str
        :param note: Текст заметки администратора API
        :type note: str
        :param del_note: ID удаляемой заметки, value будет пустым
        :type del_note: str, int


        """
        if type(order_positions) is dict:
            order_positions = [order_positions]
        if number is None and internal_number is None:
            raise AbcpParameterRequired('number and internal_number is None')
        if delivery_address_id is not None and int(delivery_address_id) == -1 and delivery_address is None:
            raise AbcpAPIError(f'Не передан новый адрес доставки')
        if delivery_cost is not None:
            logger.debug(f"{type(delivery_cost)} {type(delivery_address_id)}")
            if delivery_address_id is None:
                raise AbcpParameterRequired(
                    'Необходимо указать delivery_address_id если это существующий адрес '
                    'или delivery_address_id=-1 и новый delivery_address.')
        if delivery_address_id is not None and delivery_type_id is None:
            raise AbcpParameterRequired(
                'Необходимо передать delivery_type_id чтобы установить адрес доставки')
        if any([number, internal_number]) is not None and all(
                [order_positions, user_id, delivery_type_id, delivery_office_id, basket_id, guest_order_name,
                 guest_order_mobile, guest_order_email, shipment_date, delivery_cost, delivery_address_id,
                 delivery_address, client_order_number]) is None:
            raise AbcpParameterRequired(f'Недостаточно параметров')
        if note is not None and del_note is not None:
            raise AbcpAPIError('Заметку можно либо удалить либо добавить')

        payload = generate_payload(**locals(), order=True)

        return await self.request(api.Methods.SAVE_ORDER, payload, True)

    async def get_online_order_params(
            self,
            position_ids: Union[List, str, int]

    ):
        """Это вспомогательная операция, которую необходимо выполнять перед отправкой online-заказа поставщику. Если
        для поставщика есть дополнительные параметры заказа или позиций заказа, то в ответ вы получите набор данных.
        На их основании нужно составить API запрос для отправки заказа. Если вы уже определились с какими параметрами
        будете отправлять заказы поставщику, то эту операцию вызывать нет необходимости, можно сразу переходить к
        методу отправки заказа.
        Идентификаторы позиций, которые необходимо передавать в запросе,
        должны принадлежать одному поставщику. Т.е. за один API запрос операции cp/orders/online можно отправить
        позиции только одного поставщика. Если вам необходимо отправить позиции для двух поставщиков, то необходимо
        предварительно сгруппировать идентификаторы позиций и выполнить два запроса к cp/orders/online по каждому из
        поставщиков.
        Кол-во идентификаторов позиций в одном запросе ограничено. За один API запрос отправить в заказ можно не
        более 20 позиций для сторонних поставщиков. Для поставщиков работающих на платформе ABCP ограничение - 100
        позиций.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.B0.D1.80.D0.B0.D0.BC.D0.B5.D1.82.D1.80.D0.BE.D0.B2_.D0.B4.D0.BB.D1.8F_.D0.BE.D1.82.D0.BF.D1.80.D0.B0.D0.B2.D0.BA.D0.B8_online-.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D1.83

        :param position_ids: Массив идентификаторов позиций, которые нужно отправить поставщику (Позиции должны быть от одного поставщика)
        :type position_ids: List of ids str or int no matter

        """
        if type(position_ids) is str or type(position_ids) is int:
            position_ids = [position_ids]
        payload = generate_payload(**locals())

        return await self.request(api.Methods.GET_PARAMS_FOR_ONLINE_ORDER, payload)

    async def send_online_order(
            self,
            order_params: Union[List[Dict], Dict],
            positions: Union[List[Dict], Dict],
    ):
        """Идентификаторы позиций, которые необходимо передавать в запросе, должны принадлежать одному поставщику.
        Т.е. за один API запрос операции cp/orders/online можно отправить позиции только одного поставщика. Если вам
        необходимо отправить позиции для двух поставщиков, то необходимо предварительно сгруппировать идентификаторы
        позиций и выполнить два запроса к cp/orders/online по каждому из поставщиков. Кол-во идентификаторов позиций
        в одном запросе ограничено. За один API запрос отправить в заказ можно не более 20 позиций для сторонних
        поставщиков. Для поставщиков работающих на платформе ABCP ограничение - 100 позиций. В ответ вы можете
        получить один или несколько созданных заказов. Отправка заказа аналогична отправке из панели управления. Если
        заказ оформлен успешно, то результат фиксируется в панели управления, чекбокс заменятся на номер заказа
        поставщика и его статус (если поставщик поддерживает передачу статуса). Если настроена синхронизация
        статусов, она также активируется для отправленных позиций. Внимание! При работе с API поставщика,
        в большинстве случаев используется общая корзина при работе с сайтом поставщика и при работе с API. При
        отправке заказа поставщику последовательно выполняются запросы по предварительной очистке корзины,
        добавлению товара в корзину, чтение и отправка её в заказ. Очень важно не допустить параллельной отправки
        разных позиций одному поставщику. Так же в момент отправки заказа поставщику не должна производиться отправка
        заказов из панели управления abcp и работа с корзиной на сайте поставщика. В противном случае вы можете
        получить некорректные заказы, ошибки и задвоенные заказы с одинаковыми товарами.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D1.82.D0.BF.D1.80.D0.B0.D0.B2.D0.BA.D0.B0_online-.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D1.83
        :param order_params: Массив параметров заказа, который нужно сформировать на основе операции "Получение параметров для отправки online-заказа поставщику". Если у поставщика нет параметров заказа, то параметр orderParams необязательный.
        :type order_params: List of dict example: [{'shipmentAddress': 77333, 'comment': 'Мой коментарий', 'deliveryType': 3, 'contactName': 'Иванов Иван'}]
        :param positions: Массив данных с позициями заказов
        d = await api.get_online_order_params(id=222)
        order_params={d['orderParams'][0]['fieldName']: d['orderParams'][0]['enum'][2]['value']}, positions={'id': 263266039, 'comment': 'тест'}
        :type positions: List of ids, str or int
        """
        if type(positions) is not list:
            positions = [positions]
        if type(order_params) is dict:
            order_params = [order_params]
        payload = generate_payload_online_order(**locals())

        return await self.request(api.Methods.SEND_ONLINE_ORDER, payload, True)

    async def update_balance(
            self,
            user_id: Union[int, str],
            balance: Union[float, int, str],
            in_stop_list: Union[bool, str] = None
    ):
        """Изменяет баланс клиента. Принимает в качестве параметра текущий баланс пользователя (float) в валюте сайта
        и идентификатор пользователя на сайте. Идентификатор пользователя - это уникальное значение для всей системы,
        которое может не совпадать со значением поля "Код клиента" в карточке клиента. Узнать его можно, либо из URL
        карточки клиента, например, https://cp.abcp.ru/?page=customers&customerId=353169&action=editCustomer - в
        данном случае идентификатор клиента это значение параметра customerId, а именно, 353169; либо,
        при использовании синхронизации пользователей с помощью операции GET cp/users, идентификатор пользователя
        возвращается в поле userId.
        !!!Обновляет сальдо в карточке клиента(видно при редактировани), не влияет на модуль финансы, возможно я ошибаюсь!!!

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B1.D0.B0.D0.BB.D0.B0.D0.BD.D1.81.D0.B0_.D0.BA.D0.BB.D0.B8.D0.B5.D0.BD.D1.82.D0.B0
        :param user_id: Идентификатор пользователя на сайте, для которого обновляется баланс.
        :type user_id: int or str
        :param balance: Значение баланса в валюте сайта
        :type balance: float
        :param in_stop_list: Признак нахождения клиента в стоп-листе (необязательный параметр)
        :type in_stop_list: str or bool ('true', 'false', True, False)
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.UPDATE_BALANCE, payload, True)

    async def update_credit_limit(
            self,
            user_id: Union[int, str],
            credit_limit: Union[float, int, str]

    ):
        """Изменяет лимит кредита клиента. Принимает в качестве параметра текущий лимит кредита пользователя (float) в валюте сайта и идентификатор пользователя на сайте.
        !!!В случае успешного обновления баланса, метода возвращает:
        userId, creditLimit и excludeCart. Параметр excludeCart не указан в документации метода!!!

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BB.D0.B8.D0.BC.D0.B8.D1.82.D0.B0_.D0.BA.D1.80.D0.B5.D0.B4.D0.B8.D1.82.D0.B0_.D0.BA.D0.BB.D0.B8.D0.B5.D0.BD.D1.82.D0.B0
        :param user_id: Идентификатор пользователя на сайте, для которого обновляется баланс.
        :type user_id: int or str
        :param credit_limit: Значение лимита кредита в валюте сайта
        :type credit_limit: float
        """
        payload = generate_payload(**locals())

        return await self.request(api.Methods.UPDATE_CREDIT_LIMIT, payload, True)

    async def update_finance_info(
            self,
            user_id: Union[int, str],
            balance: Union[float, int, str] = None,
            credit_limit: float = None,
            in_stop_list: Union[bool, str] = None,
            pay_delay: Union[int, str] = None,
            overdue_saldo: Union[float, int, str] = None
    ):
        """Изменяет финансовую информацию клиента. Принимает в качестве параметров идентификатор пользователя на
        сайте и финансовую информацию пользователя. Обязательно наличие как минимум одного из полей (balance,
        creditLimit, inStopList, payDelay, overdueSaldo).

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D1.84.D0.B8.D0.BD.D0.B0.D0.BD.D1.81.D0.BE.D0.B2.D0.BE.D0.B9_.D0.B8.D0.BD.D1.84.D0.BE.D1.80.D0.BC.D0.B0.D1.86.D0.B8.D0.B8_.D0.BA.D0.BB.D0.B8.D0.B5.D0.BD.D1.82.D0.B0
        :param user_id: Идентификатор пользователя на сайте, для которого обновляется баланс.
        :type user_id: int or str
        :param balance: Значение баланса в валюте сайта
        :type balance: float
        :param credit_limit: Значение лимита кредита в валюте сайта
        :type credit_limit: float
        :param in_stop_list: Признак нахождения клиента в стоп-листе
        :type in_stop_list: str or bool ('true', 'false', True, False)
        :param pay_delay: Отсрочка платежа(в днях)
        :type pay_delay: int or str
        :param overdue_saldo: Просроченный баланс
        :type overdue_saldo: float
        """
        payload = generate_payload(**locals())

        return await self.request(api.Methods.UPDATE_FINANCE_INFO, payload, True)

    async def get_payments_info(
            self,
            user_id: Union[int, str] = None,
            payment_number: str = None,
            create_date_time_start: str = None,
            create_date_time_end: str = None
    ):
        """Возвращает список оплат из финмодуля.
        Параметры paymentNumber, userId необязательные.
        Если указан paymentNumber, то createDateTimeStart и createDateTimeEnd могут не указываться.
        Если интервал дат выбран больше года, то в ответе получаем ошибку "Сократите диапазон дат и выполните запрос снова.
        Диапазон не должен превышать 1 год."

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B8.D0.BD.D1.84.D0.BE.D1.80.D0.BC.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D0.B1_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82.D0.B0.D1.85_.D0.B8.D0.B7_.D1.84.D0.B8.D0.BD.D0.BC.D0.BE.D0.B4.D1.83.D0.BB.D1.8F
        :param user_id: Идентификатор пользователя на сайте, для которого обновляется баланс.
        :type user_id: int or str
        :param payment_number: 	Номер платежа
        :type payment_number: str
        :param create_date_time_start: example (datetime.datetime.now() - datetime.timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S") / datetime.datetime.now().strftime("%Y-%m-%d")
        :type create_date_time_start: datetime strftime("%Y-%m-%d %H:%M:%S")
        :param create_date_time_end: example (datetime.datetime.now() - datetime.timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S") / datetime.datetime.now().strftime("%Y-%m-%d")
        :type create_date_time_end: datetime strftime("%Y-%m-%d %H:%M:%S")

        """
        if all(x is None for x in [user_id, payment_number, create_date_time_start, create_date_time_end]):
            raise AbcpAPIError('Недостаточно параметров')
        if payment_number is None and any(x is None for x in [create_date_time_start, create_date_time_end]):
            raise AbcpAPIError('Недостаточно параметров')
        payload = generate_payload(**locals())

        return await self.request(api.Methods.GET_PAYMENTS, payload)

    async def get_payment_links(
            self,
            payment_numbers: Union[List, str, int] = None,
            order_ids: Union[List, str, int] = None,
            user_id: Union[int, str] = None,
            date_time_start: str = None,
            date_time_end: str = None,
    ):
        """Возвращает список привязок платежей из модуля Финансы.
        При запросе указывать либо paymentNumbers либо orderIds либо userId с DateTimeStart и DateTimeEnd.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B8.D0.BD.D1.84.D0.BE.D1.80.D0.BC.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE_.D0.BF.D1.80.D0.B8.D0.B2.D1.8F.D0.B7.D0.BA.D0.B0.D1.85_.D0.BF.D0.BB.D0.B0.D1.82.D0.B5.D0.B6.D0.B5.D0.B9_.D0.B8.D0.B7_.D0.BC.D0.BE.D0.B4.D1.83.D0.BB.D1.8F_.D0.A4.D0.B8.D0.BD.D0.B0.D0.BD.D1.81.D1.8B
        :param user_id: Идентификатор пользователя на сайте, для которого обновляется баланс.
        :type user_id: int or str
        :param payment_numbers: массив с номерами платежей [str, str, str]
        :type payment_numbers: List of str or str or int
        :param order_ids: массив с номерами заказов,если передать orderIds[]=0 и диапазон дат, то можно получить список возвратов за период
        :type order_ids: List of str or str or int
        :param date_time_start: example datetime.datetime.now().strftime("%Y-%m-%d")
        :type date_time_start: datetime strftime("%Y-%m-%d %H:%M:%S")
        :param date_time_end: example datetime.datetime.now().strftime("%Y-%m-%d")
        :type date_time_end: datetime strftime("%Y-%m-%d %H:%M:%S")

        """
        if all(x is None for x in [user_id, date_time_start, date_time_end]):
            if any(y is not None for y in [payment_numbers, order_ids]):
                pass
            else:
                raise AbcpParameterRequired(
                    f'Недостаточно параметров, укажите user_id, date_time_start, date_time_end')
        if type(order_ids) is str or type(order_ids) is int:
            order_ids = [order_ids]
        if type(payment_numbers) is str or type(payment_numbers) is int:
            payment_numbers = [payment_numbers]
        payload = generate_payload(**locals())

        return await self.request(api.Methods.GET_PAYMENTS_LINKS, payload)

    async def get_online_payments(
            self,
            date_start: str = None,
            date_end: str = None,
            customer_ids: Union[List, str, int] = None,
            payment_method_id: Union[str, int] = None,
            status_ids: Union[List, str, int] = None,
            order_ids: Union[List, str, int] = None
    ):
        """Возвращает список online платежей. Все параметры необязательные и принадлежат к параматерам filter

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_online_.D0.BF.D0.BB.D0.B0.D1.82.D0.B5.D0.B6.D0.B5.D0.B9
        :param date_start: Дата начало периода для выбора платежей. Формат: ГГГГ-ММ-ДД
        :type date_start: datetime strftime("%Y-%m-%d")
        :param date_end: Дата начало периода для выбора платежей. Формат: ГГГГ-ММ-ДД
        :type date_end: datetime strftime("%Y-%m-%d")
        :param customer_ids: Массив идентификаторов клиентов. Не более 100 штук в одном запросе.
        :type customer_ids: List or str or int
        :param payment_method_id: Идентификатор платежной системы. Получить можно из cp/users/profiles или в панели управления.
        :type payment_method_id: str or int
        :param status_ids: 	Массив идентификаторов статусов платежей:
                            1 - Начата 2 - Завершена 3 - Неудача 4 - В обработке
        :type status_ids: List or str or int
        :param order_ids: Массив идентификаторов заказов. Не более 100 штук в одном запросе.
        :type order_ids: List or str or int
        """
        if type(order_ids) is str or type(order_ids) is int:
            order_ids = [order_ids]
        if type(status_ids) is str or type(status_ids) is int:
            status_ids = [status_ids]
        if type(customer_ids) is str or type(customer_ids) is int:
            customer_ids = [customer_ids]

        payload = generate_payload_filter(**locals())

        return await self.request(api.Methods.GET_PAYMENTS_ONLINE, payload)

    async def add_multiple_payments(
            self,
            payments: Union[List[Dict], Dict] = None,
            link_payments: Union[str, int] = 0
    ):
        """Добавляет платежи клиентам. Возвращает массив добавленных платежей.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.94.D0.BE.D0.B1.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82
        :param payments: Массив идентификаторов клиентов. Не более 100 штук в одном запросе.
        :type payments: List or str or int
        :param link_payments: Идентификатор платежной системы. Получить можно из cp/users/profiles или в панели управления.
        :type link_payments: str or int
        """
        if type(payments) is dict:
            payments = [payments]
        payload = generate_payload_payments(single=False, **locals())

        return await self.request(api.Methods.ADD_PAYMENTS, payload, True)

    async def add_single_payment(
            self,
            user_id: Union[str, int],
            payment_type_id: Union[str, int],
            amount: Union[float, int],
            create_date_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            payment_number: Union[str, int] = None,
            comment: str = None,
            editor_id: Union[str, int] = None,
            link_payments: Union[str, int] = 0
    ):
        """Добавляет платежи клиентам. Возвращает массив добавленных платежей.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.94.D0.BE.D0.B1.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82
        :param user_id: Идентификатор пользователя на сайте, которому добавляется оплата
        :type user_id: int or str
        :param create_date_time: Дата и время платежа, в формате ГГГГ-ММ-ДД чч:мм:сс (например 2018-01-01 00:00:00)
        :type create_date_time: datetime strftime("%Y-%m-%d %H:%M:%S")
        :param payment_type_id: Id типа платежа
        :type payment_type_id: str or int
        :param amount: 	Сумма платежа
        :type amount: float or int
        :param payment_number: Номер платежа, максимум 64 символа. Необязательный параметр. Если передан пустой, то номер генерируется автоматически по маске переданного типа платежа
        :type payment_number: str or int
        :param comment: Комментарий к платежу (не обязательное)
        :type comment: str
        :param editor_id: Id сотрудника, которым был внесён платёж (не обязательное)
        :type editor_id: str or int
        :param link_payments: 	Параметр, отвечающий за автоматическую привязку платежей к заказам. 0 - не привязывать, 1 - привязывать
        :type link_payments: int or str

        """

        payload = generate_payload_payments(**locals())

        return await self.request(api.Methods.ADD_PAYMENTS, payload, True)

    async def delete_link_payment(
            self,
            payment_link_id: Union[str, int]
    ):
        """Удаляет привязку оплаты, увеличивает долг заказу, к которому была сделана привязка, на сумму удаляемой
        привязки, увеличивает остаток оплаты на сумму удаляемой привязки, клиенту пересчитывает сальдо и долг по
        заказам. Внимание!

        С помощью одного запроса данная операция позволяет удалить только одну привязку. Массовое удаление недоступно

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.A3.D0.B4.D0.B0.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D1.80.D0.B8.D0.B2.D1.8F.D0.B7.D0.BA.D0.B8_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82.D1.8B
        :param payment_link_id: Id привязки, которую нужно удалить.
        :type payment_link_id: int or str
        """

        payload = generate_payload(**locals())

        return await self.request(api.Methods.DELETE_PAYMENT_LINK, payload, True)

    async def link_existing_payment(
            self,
            payment_id: Union[str, int],
            order_id: Union[str, int],
            amount: Union[str, int, float]
    ):
        """Позволяет осуществлять привязку ранее созданного платежа
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D1.8F_.D0.BF.D1.80.D0.B8.D0.B2.D1.8F.D0.B7.D0.BA.D0.B8_.D0.BF.D0.BE_.D1.80.D0.B0.D0.BD.D0.B5.D0.B5_.D0.B4.D0.BE.D0.B1.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.BD.D0.BE.D0.BC.D1.83_.D0.BF.D0.BB.D0.B0.D1.82.D0.B5.D0.B6.D1.83
        :param payment_id: id платежа.
        :type payment_id: int or str
        :param order_id: id заказа по которому делается привязка.
        :type order_id: int or str
        :param amount: 	Сумма привязки.
        :type amount: str or int or float
        """

        if all(x.isdigit() for x in [payment_id, order_id, amount] if type(x) is str):
            pass
        else:
            raise AbcpAPIError('Все параметры должны являться цифрами')

        payload = generate_payload(**locals())

        return await self.request(api.Methods.LINK_EXISTING_PLAYMENT, payload, True)

    async def refund_payment(
            self,
            refund_payment_id: Union[str, int],
            refund_amount: Union[str, int, float]
    ):
        """Позволяет осуществлять возврат ранее созданного платежа
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D1.8F_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BB.D0.B0.D1.82.D0.B5.D0.B6.D0.B0
        :param refund_payment_id: id платежа.
        :type refund_payment_id: int or str
        :param refund_amount: Сумма возврата.
        :type refund_amount: int or str or float
        """
        if all(x.isdigit() for x in [refund_payment_id, refund_amount] if type(x) is str):
            pass
        else:
            raise AbcpAPIError('Все параметры должны являться цифрами')
        payload = generate_payload(**locals())
        return await self.request(api.Methods.REFUND_PAYMENT, payload, True)

    async def get_receipts(
            self,
            shop_id: Union[str, int] = None,
            queue_id: Union[str, int] = None,
            date_created_start: str = None,
            date_created_end: str = None,
            calculation_method: Union[str, int] = None,
            print_paper_check: Union[str, int] = None,
            vat: Union[str, int] = None,
            calculation_subject: Union[str, int] = None,
            payment_type: Union[str, int] = None,
            type: Union[str, int] = None,
            tax_system: Union[str, int] = None,
            intent: Union[str, int] = None,
            fiscalization: Union[str, int] = None,
            employee_id: Union[str, int] = None,
            client_id: Union[str, int] = None,
            start: Union[str, int] = None,
            rows_on_page: Union[str, int] = None,
    ):
        """Позволяет получить данные о чеках Комтет.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.87.D0.B5.D0.BA.D0.BE.D0.B2
        :param shop_id: ID магазина
        :type shop_id: int or str
        :param queue_id: ID очереди
        :type queue_id: int or str
        :param date_created_start: Начальная дата создания чека в формате ГГГГ-ММ-ДД.
        :type date_created_start: int or str
        :param date_created_end: Конечная дата создания чека в формате ГГГГ-ММ-ДД.
        :type date_created_end: int or str
        :param calculation_method: Способ расчета: 0 - Предоплата 100%, 1 - Предоплата, 2 - Полный расчет, 3 - Аванс, 4 - Частичный расчет и кредит, 5 - Оплата кредита, 6 - Передача в кредит.
        :type calculation_method: int or str
        :param print_paper_check: Был ли запрос печати бумажного чека: 0 - Нет, 1 - Да.
        :type print_paper_check: int or str
        :param vat: Налог: 5 - Без НДС, 0 - НДС по ставке 0%, 3 - НДС чека по расчетной ставке 10/110, 4 - НДС чека по расчетной ставке 20/120.
        :type vat: int or str
        :param calculation_subject: Предмет расчета: 0 -товар, 1 - работа, 2 - услуга, 3 - платеж.
        :type calculation_subject: int or str
        :param payment_type: 	Оплата: 0 - Безналичными, 1 - Наличными, 2 - Предоплата, 3 - Постоплата, 4 - Встречное предоставление.
        :type payment_type: int or str
        :param type: Тип чека: 0 - чек, 1- чек коррекции.
        :param tax_system: Система налогообложения: 0 - ОСН, 1 - УСН доход, 2 - УСН доход - расход, 3 - ЕНВД, 4 - ЕСН, 5 - Патент.
        :type tax_system: int or str
        :param intent: Направление платежа: 0 - Приход, 1 - Расход, 2 - Возврат прихода, 3 - Возврат расхода.
        :type intent: int or str
        :param fiscalization: Фискализирован: 0 - Нет, 1 - Да.
        :type fiscalization: int or str
        :param employee_id: id сотрудника, отправившего чек.
        :type employee_id: int or str
        :param client_id: 	id клиента.
        :type client_id: int or str
        :param start: Отсчет чеков
        :type start: int or str
        :param rows_on_page: 	Количество "на странице"
        :type rows_on_page: int or str


        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_RECEIPTS, payload)

    async def get_users(
            self,
            date_registred_start: Optional[str] = None,
            date_registred_end: Optional[str] = None,
            date_updated_start: Optional[str] = None,
            date_updated_end: Optional[str] = None,
            state: Union[str, int] = None,
            customer_status: Union[str, int] = None,
            customers_ids: Union[List, str, int] = None,
            market_type: Union[str, int] = None,
            phone: Union[str, int] = None,
            email: str = None,
            safe_mode: Union[str, int] = None,
            format: str = None,
            limit: int = None,
            skip: Optional[int] = None,
            desc: Union[str] = 'false'
    ):
        """Принимает в качестве параметров условия фильтрации клиентов. Возвращает список клиентов.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.BB.D0.B5.D0.B9
        :param date_registred_start: Начальная дата регистрации в формате ГГГГ-ММ-ДД ЧЧ:мм:СС
        :type date_registred_start: str datetime
        :param date_registred_end: Конечная дата регистрации в формате ГГГГ-ММ-ДД ЧЧ:мм:СС
        :type date_registred_end: str datetime
        :param date_updated_start: Начальная дата последнего обновления в формате ГГГГ-ММ-ДД ЧЧ:мм:СС
        :type date_updated_start: str datetime
        :param date_updated_end: Конечная дата последнего обновления в формате ГГГГ-ММ-ДД ЧЧ:мм:СС
        :type date_updated_end: str datetime
        :param state: Состояние клиента. Значения:-1 - отклоненный, 0 - ожидает регистрации, 1 - зарегистрированный,
                       2 - удаленный.
        :type state: int or str
        :param customer_status: Идентификатор статуса покупателя, если указать 0 - будут выбраны пользователи без статуса
        :type customer_status: int or str
        :param customers_ids: Массив идентификаторов покупателей
        :type customers_ids: List of str or int
        :param market_type: Тип регистрации. Значения:  1 - Розница 2 - Опт
        :type market_type: int or str
        :param phone: Номер телефона клиента
        :type phone: str 79998887766
        :param email: E-mail клиента
        :type email: str
        :param safe_mode: "Безопасный режим" для клиентов не имеющих поддержки формата JSON.
                Может принимать значения 0 или 1. При включении (1), адреса доставки в ответе будут возвращаться в виде
                массива объектов с полями "id" и "name", а не как "ключ - значение".
        :type safe_mode: int or str
        :param format: 	Формат ответа. Доступные значения: p - заказы содержатся в поле items,
                        данные о количестве содержатся в поле count
        :type format: str
        :param limit: Количество возвращаемых записей заказов (число, по умолчанию - 1000).
                      Чтобы получить информацию о количестве записей используйте параметр format со значением p
        :type limit: int or str
        :param skip: кол-во заказов, которые нужно пропустить. (число, по умолчанию - 0).
        :type skip: int or str
        :param desc: Обратное направление сортировки
        :type desc: str or bool ('true', 'false', True, False)


        """
        if type(customers_ids) is not list and customers_ids is not None:
            customers_ids = [customers_ids]
        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_USERS_LIST, payload)

    async def create_user(
            self,
            market_type: Union[str, int],
            name: str, password: str,
            mobile: Union[str, int],
            filial_id: Union[str, int] = None,
            second_name: str = None, surname: str = None,
            birth_date: str = None,
            member_of_club: str = None, office: Union[str, int] = None,
            email: str = None, icq: str = None, skype: str = None,
            region_id: str = None, city: str = None,
            organization_name: str = None, business: Union[str, int] = None,
            organization_form: str = None, organization_official_name: str = None,
            inn: Union[str, int] = None, kpp: Union[str, int] = None,
            ogrn: Union[str, int] = None, organization_official_address: str = None,
            bank_name: str = None, bik: Union[str, int] = None,
            correspondent_account: Union[str, int] = None, organization_account: Union[str, int] = None,
            delivery_address: str = None, comment: str = None, profile_id: str = None
    ):
        """Принимает параметры для регистрации пользователя. Осуществляет регистрацию нового пользователя в системе. Возвращает статус выполнения операции регистрации, учетные данные нового пользователя, а так же сообщение об ошибке в случае возникновения таковой.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.BB.D1.8F
        :param market_type: Тип регистрации: 1 - Розница, 2 - Опт
        :type market_type: str or int
        :param filial_id: Код филиала (если имеются)
        :type filial_id: int or str

        :param name: Имя :type name: str
        :param password: Пароль :type password: str
        :param second_name: Отчество :type second_name: str
        :param surname: Фамилия :type surname: str
        :param birth_date: Отчество :type birth_date: str datetime strftime("%Y-%m-%d %H:%M:%S")
        :param mobile: Отчество :type mobile: str or int forman 79998887766
        :param member_of_club: Название автоклуба :type member_of_club: str
        :param office: Идентификатор офиса :type office: str or int
        :param email: Отчество :type email: str
        :param icq: icq :type icq: str
        :param skype: Skype :type skype: str
        :param region_id: Код региона :type region_id: str
        :param city: Город :type city: str
        :param name: Имя :type name: str
        :param organization_name: Наименование организации :type organization_name: str
        :param business: Тип организации. Значение от 1 до 3: 1 - Автосервис, 2 - Автомагазин, 3 - Собственный автопарк
        :type business: str or int
        :param organization_form: Правовая форма организации. Варианты: ООО, ОАО, ЗАО, ТОО, АО, ЧП, ПБОЮЛ
        :type organization_form: str
        :param organization_official_name: Наименование по регистрации (без правовой формы юр. лица)
        :type organization_official_name: str
        :param inn: ИНН :type inn: str
        :param kpp: КПП :type kpp: str
        :param ogrn: ОГРН :type ogrn: str
        :param organization_official_address: Юридический адрес организации :type organization_official_address: str
        :param bank_name: Наименование банка :type bank_name: str
        :param bik: БИК банка :type bik: str or int
        :param correspondent_account: Корреспондентский счет банка :type correspondent_account: str or int
        :param organization_account: Расчетный счет организации :type organization_account: str or int
        :param delivery_address: Адрес доставки :type delivery_address: str
        :param comment: Комментарий :type comment: str
        :param profile_id: Идентификатор профиля.
        Если не указан, будет выставлен профиль по умолчанию для соответствующего типа регистрации (опт или розница).
        :type profile_id: str



        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.CREATE_USER, payload, True)

    async def get_profiles(
            self,
            format: str = None
    ):
        """Возвращает список всех профилей.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D1.80.D0.BE.D1.84.D0.B8.D0.BB.D0.B5.D0.B9
        :param format: Формат ответа. Необязательное значение
        Может принимать значения: "distributors" - выводить информацию по наценкам на поставщиков; "brands" - выводить информацию по наценкам на поставщиков и бренды
        :type format: str 'distributors' or 'brands'
        """

        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_PROFILES, payload)

    async def edit_profile(
            self,
            profile_id: Union[str, int] = None,
            code: Union[str, int] = None,
            name: str = None,
            comment: str = None,
            price_up: Union[str, int] = None,
            payment_methods: str = None,
            matrix_price_ups: Union[List[Dict], Dict] = None,
            distributors_price_ups: Union[List[Dict], Dict] = None

    ):

        """Изменяет профиль. Принимает в качестве параметров идентификатор профиля на сайте и всю информацию о профиле,
        возвращаемую операцией cp/users/profiles в формате brands.
        Работает только при выключенной опции Профили: использовать групповое сохранение, иначе возвращает ошибку.
        Если не указать идентификатор профиля, будет создан новый.
        В данном случае, обязательными параметрами будут name и priceUp.
        При создании профиля невозможно использовать имя и код существующих профилей.
        Обязательно наличие как минимум одного из полей (code, name, comment, priceUp, paymentMethods, matrixPriceUps, distributorsPriceUps).
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D1.80.D0.BE.D1.84.D0.B8.D0.BB.D1.8F
        :param profile_id: Идентификатор профиля
        :type profile_id: str or int
        :param code: Код профиля
        :type code: str or int
        :param name: Наименование профиля
        :type name: str
        :param comment: Комментарий
        :type comment: str
        :param price_up: Наценка, %
        :type price_up: str or int
        :param payment_methods: 	Платежные системы
        :type payment_methods: str or int
        :param matrix_price_ups: Идентификатор профиля
        :type matrix_price_ups: str or int
        :param distributors_price_ups: Идентификатор профиля
        :type distributors_price_ups: str or int
        """
        if type(matrix_price_ups) is dict:
            matrix_price_ups = [matrix_price_ups]
        if type(distributors_price_ups) is dict:
            distributors_price_ups = [distributors_price_ups]

        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_PROFILES, payload, True)

    async def edit_user(
            self,
            user_id: Union[str, int], business: Union[str, int] = None,
            email: str = None, second_name: str = None,
            surname: str = None, password: str = None,
            birth_date: str = None, city: str = None,
            mobile: Union[str, int] = None, icq: str = None,
            skype: str = None, state: Union[str, int] = None,
            profile_id: Union[str, int] = None, organization_name: str = None,
            organization_form: str = None, organization_official_name: str = None,
            bank_name: str = None, bik: Union[str, int] = None,
            correspondent_account: Union[str, int] = None, organization_account: Union[str, int] = None,
            delivery_address: Union[List[Dict], Dict] = None, baskets: Union[List[Dict], Dict] = None,
            baskets_delivery_address: Union[List[Dict], Dict] = None, comment: str = None,
            manager_comment: str = None, manager_id: Union[str, int] = None,
            user_code: Union[str, int] = None, client_service_employee_id: Union[str, int] = None,
            client_service_employee2_id: Union[str, int] = None, client_service_employee3_id: Union[str, int] = None,
            client_service_employee4_id: Union[str, int] = None, office: Union[List[Dict], Dict] = None,
            info: str = None, safe_mode: Union[str, int] = None

    ):

        """Осуществляет обновление данных пользователя, присланных в запросе.
        При изменении данных пользователя необязательно передавать все параметры.
        Используйте в запросе только те данные, которые вы собираетесь изменить.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B4.D0.B0.D0.BD.D0.BD.D1.8B.D1.85_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param user_id:
        :param business:
        :param email:
        :param second_name:
        :param surname:
        :param password:
        :param birth_date:
        :param city:
        :param mobile:
        :param icq:
        :param skype:
        :param state:
        :param profile_id:
        :param organization_name:
        :param organization_form:
        :param organization_official_name:
        :param bank_name:
        :param bik:
        :param correspondent_account:
        :param organization_account:
        :param delivery_address:
        :param baskets:
        :param baskets_delivery_address:
        :param comment:
        :param manager_comment:
        :param manager_id:
        :param user_code:
        :param client_service_employee_id:
        :param client_service_employee2_id:
        :param client_service_employee3_id:
        :param client_service_employee4_id:
        :param office:
        :param info:
        :param safe_mode:
        :return:
        """

        payload = generate_payload(**locals())
        return await self.request(api.Methods.EDIT_USER, payload, True)

    async def get_user_shipment_address(self, user_id: Union[str, int]):
        """Возвращает список доступных адресов доставки. Идентификатор адреса доставки необходим при отправке заказа.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B0.D0.B4.D1.80.D0.B5.D1.81.D0.BE.D0.B2_.D0.B4.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D0.BA.D0.B8
        :param user_id: Идентификатор клиента
        :type user_id: str or int
        """

        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_USER_SHIPMENT_ADDRESS, payload)

    async def get_staff(self):
        """Возвращает список менеджеров.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D0.BE.D1.82.D1.80.D1.83.D0.B4.D0.BD.D0.B8.D0.BA.D0.BE.D0.B2
        """
        return await self.request(api.Methods.GET_STAFF)

    async def get_statuses(self):
        """Возвращает список всех статусов позиций заказов.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.BE.D0.B2
        """
        return await self.request(api.Methods.GET_STATUSES)

    async def get_brands(self):
        """Возвращает список всех брендов зарегистрированных в системе с их синонимами.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D1.80.D0.B0.D0.B2.D0.BE.D1.87.D0.BD.D0.B8.D0.BA.D0.B0_.D0.B1.D1.80.D0.B5.D0.BD.D0.B4.D0.BE.D0.B2
        """
        return await self.request(api.Methods.GET_BRANDS)

    async def get_distributors(self, distributors4mc: Union[str, int] = None):
        """Возвращает список всех поставщиков, подключенных в ПУ/Поставщики.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2
        :param distributors4mc: При передаче "1" возвращает дополнительно поставщиков 4mycar"
        :type distributors4mc: str or int
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_DISTRIBUTORS_LIST, payload)

    async def edit_distributor_status(self, distributor_id: Union[str, int], status: Union[str, int]):
        """Изменение статуса поставщика
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        :param distributor_id: 	Id поставщика
        :type distributor_id: str or int
        :param status: 	1 - Вкл. \ 0 - Выкл.
        :type status: str or int
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.EDIT_DISTRIBUTORS_STATUS, payload, True)

    async def get_distributor_routes(self, distributor_id: Union[str, int]):
        """Возвращает список всех маршрутов поставщика.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.BE.D0.B2_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        :param distributor_id: 	Идентификатор поставщика
        :type distributor_id: str or int
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_SUPPLIER_ROUTES, payload)

    async def edit_distributor_route(self,
                                     route_id: Union[str, int],
                                     deadline: Union[str, int] = None, deadline_replace: str = None,
                                     is_deadline_replace_franch_enabled: Union[str, bool] = None,
                                     deadline_max: Union[str, int] = None,
                                     normal_time_start: str = None, normal_time_end: str = None,
                                     normal_days_of_week: List[str] = None,
                                     abnormal_deadline: Union[str, int] = None,
                                     abnormal_deadline_max: Union[str, int] = None,
                                     p1: Union[str, int] = None, p2: Union[str, int] = None,
                                     price_per_kg: Union[str, int] = None,
                                     price_up_added: Union[str, int] = None,
                                     c1: Union[str, int] = None,
                                     price_up_min: Union[str, int] = None, price_up_max: Union[str, int] = None,
                                     primary_price_up_to_contractor: Union[str, int] = None,
                                     delivery_probability: Union[str, int] = None,
                                     description: str = None,
                                     enable_color: Union[str, bool] = None, color: str = None,
                                     is_abnormal_color_enabled: Union[str, bool] = None, abnormal_color: str = None,
                                     no_return: Union[bool, str] = None,
                                     supplier_code_enabled_list: Union[List[str], List[int], str, int] = None,
                                     supplier_code_disabled_list: Union[List, List[int], str, int] = None,
                                     normal_time_display_only: Union[int, str] = None,
                                     disable_order_abnormal_time: Union[int, str] = None,
                                     not_user_online_supplier_deadline: Union[int, str] = None,
                                     ):
        """Осуществляет обновление данных маршрута поставщика, присланных в запросе.
        При изменении данных маршрута необязательно передавать все параметры.
        Используйте в запросе только те данные, которые вы собираетесь изменить.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B4.D0.B0.D0.BD.D0.BD.D1.8B.D1.85_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        :param route_id: Идентификатор маршрута поставщика
        :type route_id: int or str
        :param deadline: Срок поставки (часов)
        :type deadline: int or str
        :param deadline_replace: Текстовое значение для "Срока поставки"
        :type deadline_replace: str
        :param is_deadline_replace_franch_enabled: Передавать текстовое значение для "Срока поставки" франчайзи
        :type is_deadline_replace_franch_enabled: bool or str
        :param deadline_max: Максимальный срок поставки (часов)
        :type deadline_max: int or str
        :param normal_time_start:Начало рабочего времени (09:00)
        :type normal_time_start: str
        :param normal_time_end:Конец рабочего времени (09:00)
        :type normal_time_end: str
        :param normal_days_of_week:Стандартные дни недели ['Вт', 'Ср']
        :type normal_days_of_week: list
        :param abnormal_deadline:Срок поставки (вне стандартного времени)
        :param abnormal_deadline_max:	Максимальный срок поставки (вне стандартного времени)
        :param p1: Первичная наценка 10
        :type p1: str or int
        :param p2: Вторичная наценка
        :type p2: str or int
        :param price_per_kg: Стоимость 1КГ (в валюте поставщика) 200
        :type price_per_kg: str or int
        :param price_up_added:Добавочная наценка 3
        :type price_up_added: str or int
        :param c1: Коэффициент наценки 0 - 100
        :type c1: str or int
        :param price_up_min:Минимальная наценка
        :type price_up_min:int or str
        :param price_up_max:Максимальная наценка
        :type price_up_max:int or str
        :param primary_price_up_to_contractor:Приоритетная (если выше) наценка для клиента
        :type primary_price_up_to_contractor: int or str
        :param delivery_probability:Вероятность поставки (в процентах) %
        :type delivery_probability: int or str
        :param description:Краткое описание маршрута
        :type description: str
        :param enable_color:Выделять цветом 'false' or False
        :type enable_color: bool or str
        :param color: Цвет в HEX
        :type color: str
        :param is_abnormal_color_enabled: 	Выделять цветом в нерабочее время 'false' or False
        :type is_abnormal_color_enabled: bool or str
        :param abnormal_color:Цвет в HEX
        :type abnormal_color: str
        :param no_return:Без возврата 'false' or False
        :type no_return: bool or str
        :param supplier_code_enabled_list: Ограничить выдачу складами (массив)
        :type supplier_code_enabled_list list or str
        :param supplier_code_disabled_list: Исключить позиции по складам (массив)
        :type supplier_code_disabled_list list or str
        :param normal_time_display_only:Показывать только в стандартное время (0 - Нет, 1 - Да)
        :type normal_time_display_only: int or str
        :param disable_order_abnormal_time:Блокировать отправку заказа в нестандартное время (0 - Нет, 1 - Да). "1" сохраняется только при normalTimeDisplayOnly=1.
        :type disable_order_abnormal_time: int or str
        :param not_user_online_supplier_deadline: Не использовать срок поставки online-поставщика (0 - Нет, 1 - Да)
        :type not_user_online_supplier_deadline: int or str
        :return: dict
        """
        if supplier_code_enabled_list is not None and type(supplier_code_enabled_list) is not list:
            supplier_code_enabled_list = [supplier_code_enabled_list]
        if supplier_code_disabled_list is not None and type(supplier_code_disabled_list) is not list:
            supplier_code_disabled_list = [supplier_code_disabled_list]
        payload = generate_payload(**locals())

        return await self.request(api.Methods.UPDATE_ROUTE, payload, True)

    async def edit_route_status(self, route_id: Union[str, int], status: Union[str, int]):
        """Изменяет статус маршрута поставщика
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0

        :param route_id:	Идентификатор маршрута поставщика
        :type route_id: int or str
        :param status:  Значение нового статуса (1-вкл., 0-выкл.)
        :type route_id: int or str
        :return: dict
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.UPDATE_ROUTE_STATUS, payload, True)

    async def delete_route(self, route_id: Union[int, str]):
        """Удаляет маршрут поставщика.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.A3.D0.B4.D0.B0.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0

        :param route_id:Идентификатор маршрута поставщика
        :type route_id: int or str
        :return: dict
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.DELETE_ROUTE, payload, True)

    async def edit_distributor_status_office(self, office_id: Union[str, int],
                                             distributors: Union[List[Dict], Dict] = None):
        """Подключение/отключение поставщиков к офисам
        Если параметр distributors не указан или содержит пустой список все поставщики офиса будут отключены
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.B4.D0.BA.D0.BB.D1.8E.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2_.D0.BA_.D0.BE.D1.84.D0.B8.D1.81.D1.83
        :param office_id: Идентификатор офиса.
        :type office_id: int or str
        :param distributors: Массив поставщиков, если параметр не передан или содержит пустое значение - отключаются все поставщики указанного офиса.
        :type distributors List[Dict] or Dict
        :return: dict
        """
        if type(distributors) is dict:
            distributors = [distributors]
        payload = generate_payload(**locals())
        return await self.request(api.Methods.EDIT_SUPPLIER_STATUS_FOR_OFFICE, payload, True)

    async def get_office_distributors(self, office_id: Union[str, int] = None):
        """Возвращает информацию о подключенных к офису поставщиках
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2_.D0.BE.D1.84.D0.B8.D1.81.D0.B0
        :param office_id: Идентификатор офиса. Если параметр не указан то в ответе возвращаются данные по всем офисам
        :type office_id: str or int
        :return:dict
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_OFFICE_SUPPLIERS, payload)

    async def get_updated_cars(self, date_updated_start: str = None, date_updated_end: str = None):
        """Возвращает информацию об автомобилях, в которые были внесены изменения за определённый период времени.
        Если не переданы dateUpdatedStart и dateUpdatedEnd, то будет предоставлена информация за последний месяц.
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2_.D0.BE.D1.84.D0.B8.D1.81.D0.B0

        :param date_updated_start: Начальная дата последнего обновления в формате ГГГГ-ММ-ДД ЧЧ:мм:СС
        :type date_updated_start: str lambda datetime strftime("%Y-%m-%d %H:%M:%S")
        :param date_updated_end: Конечная дата последнего обновления заказа в формате ГГГГ-ММ-ДД ЧЧ:мм:СС
        :type date_updated_end: str datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        :return:dict
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_USERS_CARS, payload)

    async def get_payments_methods(self, only_enabled: Union[bool, str] = None,
                                   only_disabled: Union[bool, str] = None,
                                   payment_method_id: Union[str, int] = None):
        """Возвращает настройки платёжных систем.
        Если не указывать доп. параметры,
        то будут возвращены все существующие настройки для всех платёжных систем (активных и отключенных).
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BD.D0.B0.D1.81.D1.82.D1.80.D0.BE.D0.B5.D0.BA_.D0.BF.D0.BB.D0.B0.D1.82.D1.91.D0.B6.D0.BD.D1.8B.D1.85_.D1.81.D0.B8.D1.81.D1.82.D0.B5.D0.BC
        :param only_enabled:если true, то будет возвращён список только включенных настроек ПС
        :type only_enabled: bool or str
        :param only_disabled: если true, то будет возвращён список только выключенных настроек ПС
        :param payment_method_id: id конкретной платёжной системы для которой нужно получить настройки
        :type payment_method_id: str or int
        :return:dict
        """
        if all(x is not None for x in [only_enabled, only_disabled]):
            raise AbcpAPIError('Укажите только один параметр или only_enabled или only_disabled')
        payload = generate_payload(**locals())
        return await self.request(api.Methods.GET_PAYMENTS_SETTINGS, payload)

    ##### CLIENT API

    async def search_articles(self,
                              number: Union[str, int],
                              brand: Union[str, int],
                              use_online_stocks: int = 0,
                              disable_online_filtering: int = 0,
                              with_out_analogs: int = 1,
                              profile_id: Union[str, int] = None):
        """

        :param number:
        :param brand:
        :param use_online_stocks:
        :param disable_online_filtering:
        :param with_out_analogs:
        :param profile_id:
        :return:
        """
        if self._admin is False and profile_id is not None:
            raise NotEnoughRights('Только API Администор может указывать Профиль пользователя')

        payload = generate_payload(**locals())
        return await self.request(api.Methods.Client.SEARCH_ARTICLES, payload)

    async def basket_add(self, basket_positions: Union[List[Dict], Dict]):
        if type(basket_positions) is dict:
            basket_positions = [basket_positions]
        payload = generate_payload(**locals())

        return await self.request(api.Methods.Client.BASKET_ADD, payload, True)

    async def basket_order(self,
                           payment_method: str = None,
                           shipment_method: str = None,
                           shipment_address: str = None,
                           shipment_office: str = None,
                           shipment_date: str = None,
                           comment: str = None,
                           basket_id: str = None,
                           whole_order_only: int = 0,
                           position_ids: List = None,
                           client_order_number: Union[str, int] = None):
        """
        :param payment_method:
        :param shipment_method:
        :param shipment_address:
        :param shipment_office:
        :param shipment_date:
        :param comment:
        :param basket_id:
        :param whole_order_only:
        :param position_ids:
        :param client_order_number:
        :return:
        """
        if payment_method is None:
            payment_method = self._payment_method
        if shipment_method is None:
            shipment_method = self._shipment_method
        if shipment_address is None:
            shipment_address = self._shipment_address
        payload = generate_payload(**locals())
        return await self.request(api.Methods.Client.BASKET_ORDER, payload, True)

    async def get_client_orders(self, format: str = None, skip: int = 0, limit: int = 100):
        if format == 'p' or format is None:
            pass
        else:
            raise AbcpAPIError('Параметр format может принимать только значение "p"')
        payload = generate_payload(**locals())
        return await self.request(api.Methods.Client.GET_ORDERS, payload)

    async def set_client_params(self,
                                shipment_address_index: int,
                                shipment_method_index: int,
                                payment_method_index: int):
        shipment_address = await self.get_client_shipment_address()  # 1
        shipment_method = await self.get_client_shipment_method()  # 0
        payment_method = await self.get_client_payment_method()  # 0
        try:
            self._shipment_address = shipment_address[shipment_address_index]['id']
            self._shipment_method = shipment_method[shipment_method_index]['id']
            self._payment_method = payment_method[payment_method_index]['id']
            logger.info(f'Установлены параметры клиента по умолчанию:\n'
                        f'shipment_address:\n'
                        f'id - {shipment_address[shipment_address_index]["id"]}\n'
                        f'name - {shipment_address[shipment_address_index]["name"]}\n'
                        f'shipment_method:\n'
                        f'id - {shipment_method[shipment_method_index]["id"]}\n'
                        f'name - {shipment_method[shipment_method_index]["name"]}\n'
                        f'payment_method:\n'
                        f'id - {payment_method[payment_method_index]["id"]}\n'
                        f'name - {payment_method[payment_method_index]["name"]}\n'
                        )
        except KeyError:
            raise AbcpAPIError('Неверно передан один из индексов')

    async def get_client_shipment_address(self):
        return await self.request(api.Methods.Client.SHIPMENT_ADDRESS)

    async def get_client_shipment_method(self):
        return await self.request(api.Methods.Client.SHIPMENT_METHOD)

    async def get_client_payment_method(self):
        return await self.request(api.Methods.Client.PAYMENT_METHODS)

    async def register_user(self,
                            market_type: Union[str, int],
                            name: str, second_name: str, surname: str,
                            password: str, mobile: str,
                            office: Union[str, int], email: str,
                            profile_id: Union[str, int],
                            icq: Union[str, int] = None, skype: str = None,
                            region_id: Union[str, int] = None,
                            business: Union[str, int] = None,
                            organization_name: str = None,
                            organization_form: str = None,
                            organization_official_name: str = None,
                            inn: Union[str, int] = None,
                            kpp: Union[str, int] = None,
                            orgn: Union[str, int] = None,
                            organization_official_address: Union[str, int] = None,
                            bank_name: str = None,
                            bik: Union[str, int] = None,
                            correspondent_account: Union[str, int] = None,
                            organization_account: Union[str, int] = None,
                            delivery_address: str = None,
                            comment: str = None,
                            send_registration_email: Union[str, int] = None,
                            member_of_club: str = None,
                            birth_date: str = None,
                            filial_id: Union[str, int] = None,
                            ):
        payload = generate_payload(**locals())
        return await self.request(api.Methods.Client.REGISTER, payload, True)
