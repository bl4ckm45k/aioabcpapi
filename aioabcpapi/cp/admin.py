#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from io import BufferedReader
from typing import Dict, List, Optional, Union

from ..api import _Methods
from ..base import BaseAbcp
from ..exceptions import AbcpAPIError, AbcpParameterRequired, AbcpWrongParameterError
from ..utils.payload import generate_payload, generate_payload_filter, generate_payload_payments, \
    generate_payload_online_order, generate_file_payload


class AdminApi:
    def __init__(self, base: BaseAbcp):
        """
        Класс содержит методы административного интерфейса

        https://www.abcp.ru/wiki/API.ABCP.Admin
        """
        self._base = base
        self.orders = Orders(base)
        self.finance = Finance(base)
        self.users = Users(base)
        self.staff = Staff(base)
        self.statuses = Statuses(base)
        self.distributors = Distributors(base)
        self.catalog = Catalog(base)
        self.articles = Articles(base)
        self.users_catalog = UsersCatalog(base)
        self.payment = Payment(base)


class Orders:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get_orders_list(
            self,
            date_created_start: Union[str, datetime] = None,
            date_created_end: Union[str, datetime] = None,
            date_updated_start: Union[str, datetime] = None,
            date_updated_end: Union[str, datetime] = None,
            numbers: Union[str, int, List] = None,
            internal_numbers: Optional[List] = None,
            status_code: Union[str, int, List] = None,
            office_id: Union[int, str] = None,
            distributor_order_id: Union[int, str] = None,
            is_canceled: Union[int, str] = None,
            distributor_id: Union[str, int, List] = None,
            user_id: Union[int, str] = None,
            with_deleted: Union[str, bool] = None,
            format: Optional[str] = None,
            limit: Optional[int] = None,
            skip: Optional[int] = None,
            desc: Optional[bool] = None

    ):
        """Принимает в качестве параметров условия фильтрации заказов. Возвращает список заказов (в т.ч. список позиций заказа).

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.BE.D0.B2



        :param user_id: Идентификатор клиента (покупателя). В результате вернутся все заказы, сделанные указанным клиентом.
        :param date_created_start: Начальная дата размещения заказа `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_created_start: `str` or `datetime`
        :param date_created_end: Конечная дата размещения заказа
        :type date_created_end: `str` or `datetime`
        :param date_updated_start: Начальная дата последнего обновления заказа в формате `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_updated_start: `str` or `datetime`
        :param date_updated_end: Конечная дата последнего обновления заказа в формате `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_updated_end: `str` or `datetime`
        :param numbers: Массив номеров заказов
        :type numbers: list
        :param internal_numbers: Массив номеров заказов в учетной системе (например, в 1С). Используется только, если в параметрах запроса не задан numbers.
        :type internal_numbers: list
        :param status_code: Код статус позиции заказа (один или массив кодов). Будут выбраны заказы содержащие хотя бы одну позицию в данном статусе.
        :type status_code: Union[str, int, list]
        :param office_id: Идентификатор офиса (в ответе по параметру могут быть отфильтрованы заказы где этот офис выбран как самовывоз или если это офис клиента или если менеджер клиента, сделавшего заказ, относится к данному офису)
        :type office_id: int or str
        :param distributor_order_id: Идентификатор заказа у поставщика. В результате вернутся все заказы которые были отправлены поставщику под этим номером.
        :type distributor_order_id: int or str
        :param is_canceled: Флаг "Запрос на удаление позиции". 0 - запрос не был отправлен, 1 - запрос отправлен, 2 - запрос отклонен менеджером.
        :type is_canceled: int or str
        :param distributor_id: Идентификатор (один или массив идентификаторов) поставщика. В результате вернутся все заказы, содержащие хотя бы одну позицию от указанного поставщика.
        :type distributor_id: Union[str, int, list]
        :param with_deleted: Признак, возвращать ли в ответе удаленные заказы и позиции
        :type with_deleted: str or bool ('true', 'false', True, False)
        :param format: Формат ответа. Доступные значения: <br>
               additional - дописывает к заказу данные клиента при гостевом заказе; к позициям добавляет значение vinQueryIds
               <br>short - сокращенный вариант отображения без содержимого позиций заказов
               <br>count - возвращает только количество заказов по заданным условиям
               <br>status_only - возвращает только номер заказа, а в узле позиций: id, statusCode, brand, number, numberFix, code
               <br>p - заказы содержатся в поле items, данные о количестве содержатся в поле count
        :type format: str
        :param limit: Ограничение на возвращаемое кол-во
        :type limit: int
        :param skip: Сколько заказов пропустить
        :type skip: int
        :param desc: Обратный порядок
        :type desc: : bool


        """
        if isinstance(date_created_start, datetime):
            date_created_start = f'{date_created_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(date_created_end, datetime):
            date_created_end = f'{date_created_end:%Y-%m-%d %H:%M:%S}'
        if isinstance(date_updated_start, datetime):
            date_updated_start = f'{date_updated_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(date_updated_end, datetime):
            date_updated_end = f'{date_updated_end:%Y-%m-%d %H:%M:%S}'
        if isinstance(format, str) and format not in ["additional", "short", "count", "status_only", "p"]:
            raise AbcpWrongParameterError(
                'Параметр "format" должен принимать одно из значений ["additional", "short", "count", "status_only", "p"]')
        if limit is not None and not 1 <= int(limit) <= 1000:
            raise AbcpAPIError(f'The limit must be more than {limit}')
        if isinstance(status_code, (int, str)):
            status_code = [status_code]
        if not isinstance(numbers, list) and numbers is not None:
            numbers = [numbers]
        if isinstance(user_id, str) and not user_id.isdigit():
            raise AbcpAPIError(f'Параметр user_id должен быть числом')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Orders.GET_ORDERS_LIST, payload)

    async def get_order(
            self,
            number: Union[int, str] = None,
            internal_number: Union[int, str] = None,
            with_deleted: Union[str, bool] = None,
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
            raise AbcpParameterRequired(f'Один из параметров "number" или "internal_number" должен быть указан')
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Orders.GET_ORDER, payload)

    async def status_history(
            self,
            position_id: Union[int, str]

    ):
        """Принимает в качестве параметра id позиции заказа. Возвращает информацию об истории изменений статуса позиции заказа.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B8.D1.81.D1.82.D0.BE.D1.80.D0.B8.D0.B8_.D0.B8.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B9_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0


        :param position_id: Номер заказа int или str
        :type position_id int or str


        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Orders.STATUS_HISTORY, payload)

    async def create_or_edit_order(
            self,
            number: Union[int, str] = None,
            internal_number: Union[int, str] = None,
            user_id: Union[int, str] = None,
            date: Union[str, datetime] = None,
            comment: str = None,
            order_positions: Union[List[Dict], Dict] = None,
            delivery_type_id: Union[int, str] = None,
            delivery_office_id: Union[int, str] = None,
            basket_id: Union[int, str] = None,
            guest_order_name: str = None,
            guest_order_mobile: str = None,
            guest_order_email: str = None,
            shipment_date: Union[str, datetime] = None,
            delivery_cost: Union[str, int, float] = None,
            delivery_address_id: Union[int, str] = None,
            delivery_address: str = None,
            manager_id: Union[int, str] = None,
            client_order_number: str = None,
            note: str = None,
            del_note: Union[str, int] = None

    ):
        """Универсальный метод сохранения. Принимает в качестве параметра объект описывающий заказ. Для создания заказа
         от имени Гостя, необходимо передавать корректно заполненные параметры: guestOrderName и guestOrderMobile или guestOrderEmail,
          в зависимости от обязательности полей "Мобильный" или "Email" в форме создания гостевого заказа.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.A1.D0.BE.D1.85.D1.80.D0.B0.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0


        :param manager_id: id менеджера по заказу
        :param comment: Комментарий к заказу
        :param date: Дата заказа `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :param number: Онлайн-номер заказа
        :type number: int or str
        :param internal_number: Внутренний номер заказа, обязательный параметр для создания<br><br>
        :type internal_number int or str
        :param order_positions: Список словарей описывающих позиции, читайте документацию API.ABCP.Admin<br>В случае
         редактирования заказа, могут быть указаны только позиции и поля, которые требуют изменения. В случае создания
         заказа, должны быть указаны все позиции со всеми полями (кроме полей comment, supplierCode и itemKey).
         При редактировании позиций обязательна передача параметра id. Если параметр id не передан, будет добавлена новая позиция.
          При добавлении позиции все поля (кроме полей comment, supplierCode и itemKey) для нее являются обязательными. Для удаления позиции необходимо указать ей количество 0 или установить параметр delete в значение 1.<br><br>
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
        :param guest_order_name: Необязательный параметр - имя клиента для оформления заказа от имени Гостя.
         Для корректного оформления заказа под гостем должны быть указаны параметры guestOrderName и guestOrderMobile или
          guestOrderEmail.
        :type guest_order_name: str
        :param guest_order_mobile: Необязательный параметр - контактный телефон клиента для оформления заказа от имени
         Гостя. (в формате 70000000000). Для корректного оформления заказа под гостем должны быть указаны параметры
          guestOrderName и guestOrderMobile или guestOrderEmail.
        :type guest_order_mobile: str
        :param guest_order_email: Необязательный параметр - e-mail для оформления заказа от имени Гостя.
        (в формате user@domain.com). Для корректного оформления заказа под гостем должны быть указаны параметры guestOrderName и guestOrderMobile или guestOrderEmail.
        :type guest_order_email: str
        :param shipment_date: Дата доставки  `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type shipment_date: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
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
        if isinstance(shipment_date, datetime):
            shipment_date = f'{shipment_date:%Y-%m-%d %H:%M:%S}'
        if isinstance(date, datetime):
            date = f'{date:%Y-%m-%d %H:%M:%S}'
        if isinstance(order_positions, dict):
            order_positions = [order_positions]
        if number is None and internal_number is None:
            raise AbcpParameterRequired('number and internal_number is None')
        if delivery_address_id is not None and int(delivery_address_id) == -1 and delivery_address is None:
            raise AbcpAPIError('Не передан новый адрес доставки')
        if delivery_cost is not None and delivery_address_id is None:
            raise AbcpParameterRequired(
                'Необходимо указать delivery_address_id если это существующий адрес '
                'или delivery_address_id=-1 и новый delivery_address.')
        if delivery_address_id is not None and delivery_type_id is None:
            raise AbcpParameterRequired(
                'Необходимо передать delivery_type_id чтобы установить адрес доставки')
        if any(x is not None for x in [number, internal_number]) and all(
                [order_positions, user_id, delivery_type_id, delivery_office_id, basket_id, guest_order_name,
                 guest_order_mobile, guest_order_email, shipment_date, delivery_cost, delivery_address_id,
                 delivery_address, client_order_number]) is None:
            raise AbcpParameterRequired('Недостаточно параметров')
        if note is not None and del_note is not None:
            raise AbcpAPIError('Заметку можно либо удалить либо добавить')

        payload = generate_payload(exclude=['client_order_number', 'order_positions', 'note', 'del_note'], order=True,
                                   **locals())

        return await self._base.request(_Methods.Admin.Orders.SAVE_ORDER, payload, True)

    async def get_online_order_params(
            self,
            position_ids: Union[List, str, int]

    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.B0.D1.80.D0.B0.D0.BC.D0.B5.D1.82.D1.80.D0.BE.D0.B2_.D0.B4.D0.BB.D1.8F_.D0.BE.D1.82.D0.BF.D1.80.D0.B0.D0.B2.D0.BA.D0.B8_online-.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D1.83
        Это вспомогательная операция, которую необходимо выполнять перед отправкой online-заказа поставщику. Если
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


        :param position_ids: Массив идентификаторов позиций, которые нужно отправить поставщику (Позиции должны быть от одного поставщика)
        :type position_ids: List of ids str or int no matter

        """
        if not isinstance(position_ids, list):
            position_ids = [position_ids]
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Orders.ONLINE_ORDER, payload)

    async def send_online_order(
            self,
            order_params: Union[List[Dict], Dict],
            positions: Union[List[Dict], Dict],
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D1.82.D0.BF.D1.80.D0.B0.D0.B2.D0.BA.D0.B0_online-.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D1.83
        Идентификаторы позиций, которые необходимо передавать в запросе, должны принадлежать одному поставщику.
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


        :param order_params: Массив параметров заказа, который нужно сформировать на основе операции "Получение параметров для отправки online-заказа поставщику". Если у поставщика нет параметров заказа, то параметр orderParams необязательный.
        :type order_params: List of dict example: [{'shipmentAddress': 77333, 'comment': 'Мой коментарий', 'deliveryType': 3, 'contactName': 'Иванов Иван'}]
        :param positions: Массив данных с позициями заказов
        d = await api.cp.admin.get_online_order_params(id=222)
        order_params={d['orderParams'][0]['fieldName']: d['orderParams'][0]['enum'][2]['value']}, positions={'id': 263266039, 'comment': 'тест'}
        :type positions: List of ids, str or int
        """
        if not isinstance(positions, list):
            positions = [positions]

        if isinstance(order_params, dict):
            order_params = [order_params]
        payload = generate_payload_online_order(**locals())

        return await self._base.request(_Methods.Admin.Orders.ONLINE_ORDER, payload, True)


class Finance:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def update_balance(
            self,
            user_id: Union[int, str],
            balance: Union[float, int, str],
            in_stop_list: Union[bool, str] = None
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B1.D0.B0.D0.BB.D0.B0.D0.BD.D1.81.D0.B0_.D0.BA.D0.BB.D0.B8.D0.B5.D0.BD.D1.82.D0.B0
        Изменяет баланс клиента. Принимает в качестве параметра текущий баланс пользователя (float) в валюте сайта
        и идентификатор пользователя на сайте. Идентификатор пользователя - это уникальное значение для всей системы,
        которое может не совпадать со значением поля "Код клиента" в карточке клиента. Узнать его можно, либо из URL
        карточки клиента, например, https://cp.abcp.ru/?page=customers&customerId=353169&action=editCustomer - в
        данном случае идентификатор клиента это значение параметра customerId, а именно, 353169; либо,
        при использовании синхронизации пользователей с помощью операции GET cp/users, идентификатор пользователя
        возвращается в поле userId.
        !!!Обновляет сальдо в карточке клиента(видно при редактировани), не влияет на модуль финансы, возможно я ошибаюсь!!!


        :param user_id: Идентификатор пользователя на сайте, для которого обновляется баланс.
        :type user_id: int or str
        :param balance: Значение баланса в валюте сайта
        :type balance: float
        :param in_stop_list: Признак нахождения клиента в стоп-листе (необязательный параметр)
        :type in_stop_list: str or bool ('true', 'false', True, False)
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Finance.UPDATE_BALANCE, payload, True)

    async def update_credit_limit(
            self,
            user_id: Union[int, str],
            credit_limit: Union[float, int, str]

    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BB.D0.B8.D0.BC.D0.B8.D1.82.D0.B0_.D0.BA.D1.80.D0.B5.D0.B4.D0.B8.D1.82.D0.B0_.D0.BA.D0.BB.D0.B8.D0.B5.D0.BD.D1.82.D0.B0
        Изменяет лимит кредита клиента. Принимает в качестве параметра текущий лимит кредита пользователя (float) в валюте сайта и идентификатор пользователя на сайте.
        !!!В случае успешного обновления баланса, метода возвращает:
        userId, creditLimit и excludeCart. Параметр excludeCart не указан в документации метода!!!


        :param user_id: Идентификатор пользователя на сайте, для которого обновляется баланс.
        :type user_id: int or str
        :param credit_limit: Значение лимита кредита в валюте сайта
        :type credit_limit: float
        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Finance.UPDATE_CREDIT_LIMIT, payload, True)

    async def update_finance_info(
            self,
            user_id: Union[int, str],
            balance: Union[float, int, str] = None,
            credit_limit: float = None,
            in_stop_list: Union[bool, str] = None,
            pay_delay: Union[int, str] = None,
            overdue_saldo: Union[float, int, str] = None
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D1.84.D0.B8.D0.BD.D0.B0.D0.BD.D1.81.D0.BE.D0.B2.D0.BE.D0.B9_.D0.B8.D0.BD.D1.84.D0.BE.D1.80.D0.BC.D0.B0.D1.86.D0.B8.D0.B8_.D0.BA.D0.BB.D0.B8.D0.B5.D0.BD.D1.82.D0.B0
        Изменяет финансовую информацию клиента. Принимает в качестве параметров идентификатор пользователя на
        сайте и финансовую информацию пользователя. Обязательно наличие как минимум одного из полей (balance,
        creditLimit, inStopList, payDelay, overdueSaldo).


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

        return await self._base.request(_Methods.Admin.Finance.UPDATE_FINANCE_INFO, payload, True)

    async def get_payments_info(
            self,
            user_id: Union[int, str] = None,
            payment_number: str = None,
            create_date_time_start: Union[str, datetime] = None,
            create_date_time_end: Union[str, datetime] = None
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B8.D0.BD.D1.84.D0.BE.D1.80.D0.BC.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D0.B1_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82.D0.B0.D1.85_.D0.B8.D0.B7_.D1.84.D0.B8.D0.BD.D0.BC.D0.BE.D0.B4.D1.83.D0.BB.D1.8F
        Возвращает список оплат из финмодуля.
        Параметры paymentNumber, userId необязательные.
        Если указан paymentNumber, то createDateTimeStart и createDateTimeEnd могут не указываться.
        Если интервал дат выбран больше года, то в ответе получаем ошибку "Сократите диапазон дат и выполните запрос снова.
        Диапазон не должен превышать 1 год."


        :param user_id: Идентификатор пользователя на сайте, для которого обновляется баланс.
        :type user_id: int or str
        :param payment_number: 	Номер платежа
        :type payment_number: str
        :param create_date_time_start: Начальная дата создания `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type create_date_time_start: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :param create_date_time_end: Конечная дата создания `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type create_date_time_end: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object

        """
        if isinstance(create_date_time_start, datetime):
            create_date_time_start = f'{create_date_time_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(create_date_time_end, datetime):
            create_date_time_end = f'{create_date_time_end:%Y-%m-%d %H:%M:%S}'
        if all(x is None for x in [user_id, payment_number, create_date_time_start, create_date_time_end]):
            raise AbcpAPIError('Недостаточно параметров')
        if payment_number is None and any(x is None for x in [create_date_time_start, create_date_time_end]):
            raise AbcpAPIError('Недостаточно параметров')
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Finance.GET_PAYMENTS, payload)

    async def get_payment_links(
            self,
            payment_numbers: Union[List, str, int] = None,
            order_ids: Union[List, str, int] = None,
            user_id: Union[int, str] = None,
            date_time_start: Union[str, datetime] = None,
            date_time_end: Union[str, datetime] = None,
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B8.D0.BD.D1.84.D0.BE.D1.80.D0.BC.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE_.D0.BF.D1.80.D0.B8.D0.B2.D1.8F.D0.B7.D0.BA.D0.B0.D1.85_.D0.BF.D0.BB.D0.B0.D1.82.D0.B5.D0.B6.D0.B5.D0.B9_.D0.B8.D0.B7_.D0.BC.D0.BE.D0.B4.D1.83.D0.BB.D1.8F_.D0.A4.D0.B8.D0.BD.D0.B0.D0.BD.D1.81.D1.8B
        Возвращает список привязок платежей из модуля Финансы.
        При запросе указывать либо paymentNumbers либо orderIds либо userId с DateTimeStart и DateTimeEnd.

        :param user_id: Идентификатор пользователя на сайте, для которого обновляется баланс.
        :type user_id: int or str
        :param payment_numbers: массив с номерами платежей [str, str, str]
        :type payment_numbers: List of str or str or int
        :param order_ids: массив с номерами заказов,если передать 0 и диапазон дат, то можно получить список возвратов за период
        :type order_ids: List of str or str or int
        :param date_time_start: Начальная дата `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_time_start: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :param date_time_end: Конечная дата  `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_time_end: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object

        """

        if isinstance(date_time_start, datetime):
            date_time_start = f'{date_time_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(date_time_end, datetime):
            date_time_end = f'{date_time_end:%Y-%m-%d %H:%M:%S}'
        if all(x is None for x in [user_id, date_time_start, date_time_end]):
            if any(y is not None for y in [payment_numbers, order_ids]):
                pass
            else:
                raise AbcpParameterRequired(
                    f'Недостаточно параметров, укажите user_id, date_time_start, date_time_end')
        if not isinstance(order_ids, list) and order_ids is not None:
            order_ids = [order_ids]
        if not isinstance(payment_numbers, list) and payment_numbers is not None:
            payment_numbers = [payment_numbers]
        payload = generate_payload(exclude=['date_time_start', 'date_time_end'], **locals())

        return await self._base.request(_Methods.Admin.Finance.GET_PAYMENTS_LINKS, payload)

    async def get_online_payments(
            self,
            date_start: Union[str, datetime] = None,
            date_end: Union[str, datetime] = None,
            customer_ids: Union[List, int] = None,
            payment_method_id: Union[int, str] = None,
            status_ids: Union[List, str, int] = None,
            order_ids: Union[List, str, int] = None
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_online_.D0.BF.D0.BB.D0.B0.D1.82.D0.B5.D0.B6.D0.B5.D0.B9
        Возвращает список online платежей. Все параметры необязательные и принадлежат к параматерам filter


        :param date_start: Дата начало периода для выбора платежей. `str` в формате %Y-%m-%d или %Y-%m-%d %H:%M:%S или datetime object(%Y-%m-%d)
        :type date_start: `str` в формате %Y-%m-%d или datetime object. Для
        :param date_end: Дата начало периода для выбора платежей. `str` в формате %Y-%m-%d или %Y-%m-%d %H:%M:%S или datetime object(%Y-%m-%d)
        :type date_end: `str` в формате %Y-%m-%d или datetime object
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
        if isinstance(date_start, datetime):
            date_start = f'{date_start:%Y-%m-%d}'
        if isinstance(date_end, datetime):
            date_end = f'{date_end:%Y-%m-%d}'

        if order_ids is not None and not isinstance(order_ids, list):
            order_ids = [order_ids]
        if status_ids is not None and not isinstance(status_ids, list):
            status_ids = [status_ids]
        if customer_ids is not None and not isinstance(customer_ids, list):
            customer_ids = [customer_ids]

        payload = generate_payload_filter(**locals())

        return await self._base.request(_Methods.Admin.Finance.GET_PAYMENTS_ONLINE, payload)

    async def add_multiple_payments(
            self,
            payments: Union[List[Dict], Dict] = None,
            link_payments: Union[bool, int] = 0
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.94.D0.BE.D0.B1.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82
        Добавляет платежи клиентам. Возвращает массив добавленных платежей.


        :param payments: Массив с оплатами
        :type payments: Union[List[Dict], Dict]
        :param link_payments: Идентификатор платежной системы. Получить можно из cp/users/profiles или в панели управления.
        :type link_payments: str or int
        """
        if isinstance(link_payments, bool):
            link_payments = str(link_payments)
        if type(payments) is dict:
            payments = [payments]
        payload = generate_payload_payments(single=False, **locals())

        return await self._base.request(_Methods.Admin.Finance.ADD_PAYMENTS, payload, True)

    async def add_single_payment(
            self,
            user_id: int,
            payment_type_id: int,
            amount: Union[float, int],
            create_date_time: Union[str, datetime] = None,
            payment_number: Union[str, int] = None,
            comment: Optional[str] = None,
            editor_id: Union[int, str] = None,
            link_payments: Union[bool, int] = False
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.94.D0.BE.D0.B1.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82
        Добавляет платежи клиентам. Возвращает массив добавленных платежей.


        :param user_id: Идентификатор пользователя на сайте, которому добавляется оплата
        :type user_id: int or str
        :param create_date_time: Дата и время платежа, `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type create_date_time: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
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
        if isinstance(link_payments, bool):
            link_payments = int(link_payments)
        if isinstance(create_date_time, datetime):
            create_date_time = f'{create_date_time:%Y-%m-%d %H:%M:%S}'

        payload = generate_payload_payments(**locals())

        return await self._base.request(_Methods.Admin.Finance.ADD_PAYMENTS, payload, True)

    async def delete_link_payment(
            self,
            payment_link_id: int
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.A3.D0.B4.D0.B0.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D1.80.D0.B8.D0.B2.D1.8F.D0.B7.D0.BA.D0.B8_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82.D1.8B
        Удаляет привязку оплаты, увеличивает долг заказу, к которому была сделана привязка, на сумму удаляемой
        привязки, увеличивает остаток оплаты на сумму удаляемой привязки, клиенту пересчитывает сальдо и долг по
        заказам. Внимание!

        С помощью одного запроса данная операция позволяет удалить только одну привязку. Массовое удаление недоступно


        :param payment_link_id: Id привязки, которую нужно удалить.
        :type payment_link_id: int or str
        """

        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Finance.DELETE_PAYMENT_LINK, payload, True)

    async def link_existing_payment(
            self,
            payment_id: Union[str, int],
            order_id: Union[str, int],
            amount: Union[str, int, float]
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D1.8F_.D0.BF.D1.80.D0.B8.D0.B2.D1.8F.D0.B7.D0.BA.D0.B8_.D0.BF.D0.BE_.D1.80.D0.B0.D0.BD.D0.B5.D0.B5_.D0.B4.D0.BE.D0.B1.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.BD.D0.BE.D0.BC.D1.83_.D0.BF.D0.BB.D0.B0.D1.82.D0.B5.D0.B6.D1.83
        Позволяет осуществлять привязку ранее созданного платежа


        :param payment_id: id платежа.
        :type payment_id: int or str
        :param order_id: id заказа по которому делается привязка.
        :type order_id: int or str
        :param amount: 	Сумма привязки.
        :type amount: str or int or float
        """

        if all(x.isdigit() for x in [payment_id, order_id, amount] if isinstance(x, str)):
            pass
        else:
            raise AbcpAPIError('Все параметры должны являться цифрами')

        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Finance.LINK_EXISTING_PLAYMENT, payload, True)

    async def refund_payment(
            self,
            refund_payment_id: Union[str, int],
            refund_amount: Union[str, int, float]
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D1.8F_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BB.D0.B0.D1.82.D0.B5.D0.B6.D0.B0
        Позволяет осуществлять возврат ранее созданного платежа


        :param refund_payment_id: id платежа.
        :type refund_payment_id: int or str
        :param refund_amount: Сумма возврата.
        :type refund_amount: int or str or float
        """
        if not all(x.isdigit() for x in [refund_payment_id, refund_amount] if isinstance(x, str)):
            raise AbcpAPIError('Все параметры должны являться цифрами')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Finance.REFUND_PAYMENT, payload, True)

    async def delete_payment(self, payment_id: int, delete_link: Union[int, bool] = 0):
        if isinstance(delete_link, bool):
            delete_link = int(delete_link)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Finance.DELETE_PAYMENT, payload, True)

    async def get_receipts(
            self,
            shop_id: Union[int, str] = None,
            queue_id: Union[int, str] = None,
            date_created_start: Union[str, datetime] = None,
            date_created_end: Union[str, datetime] = None,
            calculation_method: Union[str, int] = None,
            print_paper_check: Union[str, int] = None,
            vat: Union[str, int] = None,
            calculation_subject: Union[str, int] = None,
            payment_type: Union[str, int] = None,
            type: Union[str, int] = None,
            tax_system: Union[str, int] = None,
            intent: Union[str, int] = None,
            fiscalization: Union[str, int] = None,
            employee_id: Union[int, str] = None,
            client_id: Union[int, str] = None,
            start: Union[str, int] = None,
            rows_on_page: Union[str, int] = None,
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.87.D0.B5.D0.BA.D0.BE.D0.B2
        Позволяет получить данные о чеках Комтет.


        :param shop_id: ID магазина
        :type shop_id: int or str
        :param queue_id: ID очереди
        :type queue_id: int or str
        :param date_created_start: Начальная дата создания чека в формате `str` в формате %Y-%m-%d  или datetime object
        :type date_created_start: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :param date_created_end: Конечная дата создания чека `str` в формате %Y-%m-%d  или datetime object
        :type date_created_end: `str` в формате %Y-%m-%d или datetime object
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
        if isinstance(date_created_start, datetime):
            date_created_start = f'{date_created_start:%Y-%m-%d}'
        if isinstance(date_created_end, datetime):
            date_created_end = f'{date_created_end:%Y-%m-%d}'
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Finance.GET_RECEIPTS, payload)

    async def get_payments_methods(self, only_enabled: Union[bool, str] = None,
                                   only_disabled: Union[bool, str] = None,
                                   payment_method_id: Union[int, str] = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BD.D0.B0.D1.81.D1.82.D1.80.D0.BE.D0.B5.D0.BA_.D0.BF.D0.BB.D0.B0.D1.82.D1.91.D0.B6.D0.BD.D1.8B.D1.85_.D1.81.D0.B8.D1.81.D1.82.D0.B5.D0.BC
        Возвращает настройки платёжных систем.
        Если не указывать доп. параметры,
        то будут возвращены все существующие настройки для всех платёжных систем (активных и отключенных).


        :param only_enabled:если true, то будет возвращён список только включенных настроек ПС
        :type only_enabled: bool or str
        :param only_disabled: если true, то будет возвращён список только выключенных настроек ПС
        :param payment_method_id: id конкретной платёжной системы для которой нужно получить настройки
        :type payment_method_id: str or int
        :return:dict
        """
        if all(x is not None for x in [only_enabled, only_disabled]):
            raise AbcpAPIError('Укажите только один параметр должен быть указан only_enabled или only_disabled')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Finance.GET_PAYMENTS_SETTINGS, payload)


class Users:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get_users(
            self,
            date_registred_start: Union[str, datetime] = None,
            date_registred_end: Union[str, datetime] = None,
            date_updated_start: Union[str, datetime] = None,
            date_updated_end: Union[str, datetime] = None,
            state: Union[str, int] = None,
            customer_status: Union[str, int] = None,
            customers_ids: Union[List, str, int] = None,
            market_type: Union[str, int] = None,
            phone: Union[str, int] = None,
            enable_sms: Union[str, bool] = None,
            email: str = None,
            safe_mode: Union[str, int] = None,
            format: str = None,
            limit: Optional[int] = None,
            skip: Optional[int] = None,
            desc: Union[str, bool] = 'false'
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.BB.D0.B5.D0.B9
        Принимает в качестве параметров условия фильтрации клиентов. Возвращает список клиентов.


        :param date_registred_start: Начальная дата регистрации `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_registred_start: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :param date_registred_end: Конечная дата регистрации `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_registred_end: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :param date_updated_start: Начальная дата последнего обновления `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_updated_start: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :param date_updated_end: Конечная дата последнего обновления `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_updated_end: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
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
        :param enable_sms: Производится ли отпровка SMS клиенту
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

        if isinstance(date_registred_start, datetime):
            date_registred_start = f'{date_registred_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(date_registred_end, datetime):
            date_registred_end = f'{date_registred_end:%Y-%m-%d %H:%M:%S}'
        if isinstance(date_updated_start, datetime):
            date_updated_start = f'{date_updated_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(date_updated_end, datetime):
            date_updated_end = f'{date_updated_end:%Y-%m-%d %H:%M:%S}'

        if isinstance(format, str) and format != 'p':
            raise AbcpWrongParameterError('The parameter "format" can only take the value "p" or None')
        if not isinstance(customers_ids, list) and customers_ids is not None:
            customers_ids = [customers_ids]
        if isinstance(enable_sms, str) and (enable_sms != 'true' and enable_sms != 'false'):
            raise AbcpAPIError('Параметр "enable_sms" должен быть булевым значением, либо строкой "true" или "false"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.GET_USERS_LIST, payload)

    async def create(
            self,
            market_type: Union[str, int],
            name: str, password: str,
            mobile: Union[str, int],
            filial_id: Union[int, str] = None,
            second_name: str = None, surname: str = None,
            birth_date: Union[str, datetime] = None,
            member_of_club: str = None, office: Union[str, int] = None,
            email: str = None, icq: str = None, skype: str = None,
            region_id: str = None, city: str = None,
            organization_name: str = None, business: Union[str, int] = None,
            organization_form: str = None, organization_official_name: str = None,
            inn: Union[str, int] = None, kpp: Union[str, int] = None,
            ogrn: Union[str, int] = None, organization_official_address: str = None,
            bank_name: str = None, bik: Union[str, int] = None,
            correspondent_account: Union[str, int] = None, organization_account: Union[str, int] = None,
            delivery_address: str = None, comment: str = None, profile_id: str = None,
            pickup_state: Union[int, bool] = None
    ):
        """Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.BB.D1.8F
        Принимает параметры для регистрации пользователя. Осуществляет регистрацию нового пользователя в системе.
        Возвращает статус выполнения операции регистрации, учетные данные нового пользователя, а так же сообщение об ошибке в случае возникновения таковой.

        :param market_type: Тип регистрации: 1 - Розница, 2 - Опт
        :type market_type: str or int
        :param filial_id: Код филиала (если имеются)
        :type filial_id: int or str
        :param name: Имя :type name: str
        :param password: Пароль :type password: str
        :param second_name: Отчество :type second_name: str
        :param surname: Фамилия :type surname: str
        :param birth_date: Дата рождения :type birth_date: str datetime strftime("%Y-%m-%d")
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
        :param pickup_state: Запрет самовывоза для клиента. 0 - запретить самовывоз, 1- разрешить самовывоз. Параметр актуален только если у вас на сайте включена опция: "Корзина: запрет самовывоза определенным клиентам".
        """

        if isinstance(birth_date, datetime):
            birth_date = f'{birth_date:%Y-%m-%d}'
        if isinstance(pickup_state, bool):
            pickup_state = int(pickup_state)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.CREATE_USER, payload, True)

    async def get_profiles(
            self,
            profile_id: Union[int, str] = None,
            skip: Optional[int] = None,
            limit: Optional[int] = None,
            format: str = None
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D1.80.D0.BE.D1.84.D0.B8.D0.BB.D0.B5.D0.B9
        Возвращает список всех профилей.


        :param limit: Кол-во профилей в ответе. Необязательный параметр. Допустимые значения от 1 до 100. По умолчанию возвращаются все профили.
        :param skip: Кол-во профилей, которые нужно пропустить. Необязательный параметр. По умолчанию: 0.
        :param profile_id: Идентификатор профиля. Необязательный параметр. По умолчанию возвращаются все профили.
        :param format: Формат ответа. Необязательное значение
        Может принимать значения: "distributors" - выводить информацию по наценкам на поставщиков; "brands" - выводить информацию по наценкам на поставщиков и бренды
        :type format: str 'distributors' or 'brands'
        """
        format_params_check = ('brands', 'distributors')
        if isinstance(format, str) and format not in format_params_check:
            raise AbcpWrongParameterError('format parameter can take values "brands" or "distributors"')
        del format_params_check
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.GET_PROFILES, payload)

    async def edit_profile(
            self,
            profile_id: Union[int, str],
            code: Union[str, int] = None,
            name: str = None,
            comment: str = None,
            price_up: Union[str, int] = None,
            payment_methods: str = None,
            matrix_price_ups: Union[List[Dict], Dict] = None,
            distributors_price_ups: Union[List[Dict], Dict] = None,

    ):

        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D1.80.D0.BE.D1.84.D0.B8.D0.BB.D1.8F
        Изменяет профиль. Принимает в качестве параметров идентификатор профиля на сайте и всю информацию о профиле,
        возвращаемую операцией cp/users/profiles в формате brands.
        Работает только при выключенной опции Профили: использовать групповое сохранение, иначе возвращает ошибку.
        Если не указать идентификатор профиля, будет создан новый.
        В данном случае, обязательными параметрами будут name и priceUp.
        При создании профиля невозможно использовать имя и код существующих профилей.
        Обязательно наличие как минимум одного из полей (code, name, comment, priceUp, paymentMethods, matrixPriceUps, distributorsPriceUps).


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
        :param matrix_price_ups: Наценки от стоимости товара
        :type matrix_price_ups: List of dicts
        :param distributors_price_ups: Наценки по поставщикам
        :type distributors_price_ups: str or int
        """
        if all(x is None for x in [code, name, comment,
                                   price_up, payment_methods,
                                   matrix_price_ups, distributors_price_ups]):
            raise AbcpParameterRequired("Один из опциональных параметров должен быть передан")
        if isinstance(matrix_price_ups, dict):
            matrix_price_ups = [matrix_price_ups]
        if isinstance(distributors_price_ups, dict):
            distributors_price_ups = [distributors_price_ups]
        payload = generate_payload(exclude=['matrix_price_ups', 'distributors_price_ups'], **locals())
        return await self._base.request(_Methods.Admin.Users.EDIT_PROFILE, payload, True)

    async def edit(
            self,
            user_id: Union[str, int], business: Union[str, int] = None,
            email: str = None, name: str = None, second_name: str = None,
            surname: str = None, password: str = None,
            birth_date: Union[str, datetime] = None, city: str = None,
            mobile: Union[str, int] = None, icq: str = None,
            skype: str = None, enable_sms: Union[bool, str] = None, state: Union[str, int] = None,
            profile_id: Union[int, str] = None, organization_name: str = None,
            organization_form: str = None, organization_official_name: str = None,
            inn: Union[str, int] = None, kpp: Union[str, int] = None, ogrn: Union[str, int] = None,
            bank_name: str = None, bik: Union[str, int] = None,
            correspondent_account: Union[str, int] = None, organization_account: Union[str, int] = None,
            delivery_address: Union[List[Dict], Dict] = None, baskets: Union[List[Dict], Dict] = None,
            baskets_delivery_address: Union[List[Dict], Dict] = None, comment: str = None,
            manager_comment: str = None, manager_id: Union[int, str] = None,
            user_code: Union[str, int] = None, client_service_employee_id: Union[int, str] = None,
            client_service_employee2_id: Union[int, str] = None, client_service_employee3_id: Union[int, str] = None,
            client_service_employee4_id: Union[int, str] = None, office: Union[List[Dict], Dict] = None,
            info: str = None, safe_mode: Union[str, int] = None,
            pickup_state: Union[int, bool] = None,

    ):

        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B4.D0.B0.D0.BD.D0.BD.D1.8B.D1.85_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.BB.D1.8F
        Осуществляет обновление данных пользователя, присланных в запросе.
        При изменении данных пользователя необязательно передавать все параметры.
        Используйте в запросе только те данные, которые вы собираетесь изменить.


        :param ogrn: ОГРН
        :param kpp: КПП
        :param inn:ИНН
        :param name: Имя
        :param user_id: Идентификатор изменяемого клиента
        :param business: Тип организации. Значение от 1 до 6:
        :param email: Адрес электронной почты
        :param second_name:	Отчество
        :param surname: Фамилия
        :param password: Необязательный параметр. Предназначен для изменения пароля пользователя
        :param birth_date:Дата рождения `str` в формате %Y-%m-%d  или datetime object
        :param city: Город
        :param mobile: Номер мобильного телефона
        :param icq:	ICQ UIN
        :param skype: Skype
        :param enable_sms: Производится ли отпровка SMS клиенту
        :param state: Состояние аккаунта. Значения: от -1 до 2
        :param profile_id: Идентификатор профиля
        :param organization_name: Наименование организации
        :param organization_form: Правовая форма организации.
        :param organization_official_name: Наименование по регистрации (без правовой формы юр. лица)
        :param bank_name: Наименование банка
        :param bik: БИК банка
        :param correspondent_account: Корреспондентский счет банка
        :param organization_account: Расчетный счет организации
        :param delivery_address: Адреса доставки (массив, где ключи - id адресов). Если передать пустой параметр deliveryAddress, то все адреса клиента будут удалены!
        :param baskets: Корзины клиента (массив, где ключи - id корзин). Если передать пустой параметр baskets, то все корзины клиента будут удалены!
        :param baskets_delivery_address: Связки корзины и адреса доставки(массив, где ключи - id корзин). Обновятся только переданные связки "корзина - Адрес доставки". Чтобы убрать привязку корзины и адреса нужно передать значение параметра = "0".
        :param comment: Комментарий пользователя
        :param manager_comment: Комментарий менеджера
        :param manager_id: Идентификатор менеджера. Если передать managerId=0, то менеджер в карточке клиента удалится.
        :param user_code: Внутренний код пользователя
        :param client_service_employee_id: Идентификатор личного менеджера клиентской службы (дополнительная опция). Если передать clientServiceEmployeeId=0, то менеджер клиентской службы в карточке клиента удалится.
        :param client_service_employee2_id: Идентификатор личного менеджера клиентской службы (дополнительная опция). Если передать clientServiceEmployeeId=0, то менеджер клиентской службы в карточке клиента удалится.
        :param client_service_employee3_id: Идентификатор личного менеджера клиентской службы (дополнительная опция). Если передать clientServiceEmployeeId=0, то менеджер клиентской службы в карточке клиента удалится.
        :param client_service_employee4_id: Идентификатор личного менеджера клиентской службы (дополнительная опция). Если передать clientServiceEmployeeId=0, то менеджер клиентской службы в карточке клиента удалится.
        :param office: Массив идентификаторов офисов, к которым необходимо подключить клиента. Если идентификатор офиса, к одному из которых подключен клиент, не будет передан, то он будет отключен. Передать пустой параметр office нельзя, т.к. клиент должен быть подключен минимум к одному офису. Параметр актуален только если у вас на сайте включена опция: "Офисы: включить привязку к клиентам".
        :param info: "Информация" в личном кабинете. В поле допустимо использование html-тегов. max 4000 символов. Закладка появляется только если есть данные в поле info для клиента.
        :param safe_mode:
        :param pickup_state: Запрет самовывоза для клиента. 0 - запретить самовывоз, 1- разрешить самовывоз. Параметр актуален только если у вас на сайте включена опция: "Корзина: запрет самовывоза определенным клиентам".
        :return:
        """
        if isinstance(birth_date, datetime):
            birth_date = f'{birth_date:%Y-%m-%d}'
        if isinstance(pickup_state, bool):
            pickup_state = int(pickup_state)
        if isinstance(enable_sms, str) and (enable_sms != 'true' and enable_sms != 'false'):
            raise AbcpAPIError('Параметр "enable_sms" должен быть булевым значением, либо строкой "true" или "false"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.EDIT_USER, payload, True)

    async def get_user_shipment_address(self, user_id: Union[int, str]):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B0.D0.B4.D1.80.D0.B5.D1.81.D0.BE.D0.B2_.D0.B4.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D0.BA.D0.B8

        Возвращает список доступных адресов доставки. Идентификатор адреса доставки необходим при отправке заказа.

        :param user_id: Идентификатор клиента
        :type user_id: str or int
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.GET_USER_SHIPMENT_ADDRESS, payload)

    async def get_shipment_address_zones(self):
        """
        Получение списка зон адресов доставки

        :return: Возвращает список зон адресов доставки.
        """
        return await self._base.request(_Methods.Admin.Users.GET_USER_SHIPMENT_ADDRESS_ZONES)

    async def get_shipment_address_zone(self, id: int):
        """
        Получение одной зоны адресов доставки

        :param id: Уникальный идентификатор зоны адресов доставки
        :return: Возвращает одну зону адресов доставки по указанному уникальному идентификатору.
        """
        return await self._base.request(_Methods.Admin.Users.GET_USER_SHIPMENT_ADDRESS_ZONE.format(id))

    async def update_shipment_zones(self, zones: Union[List[Dict], Dict]):
        """
        Сохранение зон адресов доставки. Универсальный метод добавления и обновления зон адресов доставки.

        :param zones: Массив объектов зон адресов доставки
        :return:
        """
        if isinstance(zones, dict):
            zones = [zones]

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.UPDATE_SHIPMENT_ZONES, payload, True)

    async def create_shipment_zone(self, name: str, **kwargs):
        """
        Создание новой зоны адресов доставки. Метод создания одной зоны адресов доставки.

        :param name: Название зоны
        :param kwargs: Аргументы isOnDay{day}: int и stopTimeDay{day}: int
        :return:
        """
        if kwargs is None:
            raise AbcpParameterRequired('Необходимо передать аргументы "isOnDay{day:int}" и "stopTimeDay{day:int}"\n\n'
                                        'Например: isOnDay1=1, stopTimeDay1="15:30"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.CREATE_SHIPMENT_ZONE, payload, True, json=True)

    async def update_shipment_zone(self, id: int, name: str, **kwargs):
        """
        Метод обновления данных одной зоны адресов доставки.

        :param id: Идентификатор обновляемой зоны
        :param name: Название зоны
        :param kwargs: Аргументы isOnDay{day}: int и stopTimeDay{day}: int
        :return:
        """
        if kwargs is None:
            raise AbcpParameterRequired('Необходимо передать аргументы "isOnDay{day:int}" и "stopTimeDay{day:int}"\n\n'
                                        'Например: isOnDay1=1, stopTimeDay1="15:30"')
        _method = _Methods.Admin.Users.UPDATE_SHIPMENT_ZONE.format(id)
        del id
        payload = generate_payload(**locals())
        return await self._base.request(_method, payload, True, json=True)

    async def delete_shipment_zone(self, id: int):
        return await self._base.request(_Methods.Admin.Users.DELETE_SHIPMENT_ZONE.format(id), None, True)

    async def get_updated_cars(self, date_updated_start: str = None, date_updated_end: str = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2_.D0.BE.D1.84.D0.B8.D1.81.D0.B0
        Возвращает информацию об автомобилях, в которые были внесены изменения за определённый период времени.
        Если не переданы dateUpdatedStart и dateUpdatedEnd, то будет предоставлена информация за последний месяц.


        :param date_updated_start: Начальная дата последнего обновления `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_updated_start: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :param date_updated_end: Конечная дата последнего обновления заказа `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :type date_updated_end: `str` в формате %Y-%m-%d %H:%M:%S  или datetime object
        :return:dict
        """
        if isinstance(date_updated_start, datetime):
            date_updated_start = f'{date_updated_start:%Y-%m-%d %H:%M:%S}'

        if isinstance(date_updated_end, datetime):
            date_updated_end = f'{date_updated_end:%Y-%m-%d %H:%M:%S}'
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.GET_USERS_CARS, payload)

    async def get_sms_settings(self, user_ids: Union[List, int, str]):
        if not isinstance(user_ids, list):
            user_ids = [user_ids]
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.SMS_SETTINGS, payload)


class Staff:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D0.BE.D1.82.D1.80.D1.83.D0.B4.D0.BD.D0.B8.D0.BA.D0.BE.D0.B2
        Возвращает список менеджеров.
        """
        return await self._base.request(_Methods.Admin.Staff.GET_STAFF)

    async def update_manager(self, id: int, type_id: int = None,
                             first_name: str = None, last_name: str = None,
                             email: str = None, phone: str = None, mobile: str = None,
                             sip: Union[str, int] = None, comment: str = None, boss_id: int = None, office_id: int = None):
        """

        Обновление данных сотрудника.

        При изменении данных сотрудника необязательно передавать все параметры. Используйте в запросе только те данные, которые вы собираетесь изменить.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B4.D0.B0.D0.BD.D0.BD.D1.8B.D1.85_.D1.81.D0.BE.D1.82.D1.80.D1.83.D0.B4.D0.BD.D0.B8.D0.BA.D0.B0

        :param id: Идентификатор сотрудника (обязательное поле)
        :param type_id: Идентификатор должности сотрудника
        :param first_name: Имя сотрудника
        :param last_name: Фамилия сотрудника
        :param email: Адрес ящика электронной почты
        :param phone: Номер телефона
        :param mobile: Номер мобильного телефона
        :param sip: SIP номер
        :param comment: Комментарий
        :param boss_id: Идентификатор руководителя
        :param office_id: Идентификатор офиса
        :return:
        """
        if isinstance(sip, str) and not sip.isdigit():
            raise AbcpWrongParameterError('Параметр "SIP" должен быть числом')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Staff.UPDATE_STAFF, payload, True)


class Statuses:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.BE.D0.B2
        Возвращает список всех статусов позиций заказов.
        """
        return await self._base.request(_Methods.Admin.Statuses.GET_STATUSES)


class Articles:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get_brands(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D1.80.D0.B0.D0.B2.D0.BE.D1.87.D0.BD.D0.B8.D0.BA.D0.B0_.D0.B1.D1.80.D0.B5.D0.BD.D0.B4.D0.BE.D0.B2
        Возвращает список всех брендов зарегистрированных в системе с их синонимами.
        """
        return await self._base.request(_Methods.Admin.Articles.GET_BRANDS)

    async def get_brand_group(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D1.80.D0.B0.D0.B2.D0.BE.D1.87.D0.BD.D0.B8.D0.BA.D0.B0_.D0.B1.D1.80.D0.B5.D0.BD.D0.B4.D0.BE.D0.B2

        Возвращает список всех групп брендов зарегистрированных в системе.
        """
        return await self._base.request(_Methods.Admin.Articles.GET_BRANDS_GROUP)


class Distributors:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get(self, distributors4mc: Union[str, int, bool] = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2
        Возвращает список всех поставщиков, подключенных в ПУ/Поставщики.


        :param distributors4mc: При передаче "1" возвращает дополнительно поставщиков 4mycar"
        :type distributors4mc: str or int
        """
        if isinstance(distributors4mc, bool):
            distributors4mc = int(distributors4mc)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.GET_DISTRIBUTORS_LIST, payload)

    async def edit_status(self, distributor_id: Union[int, str], status: Union[int, bool]):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        Изменение статуса поставщика


        :param distributor_id: 	Id поставщика
        :type distributor_id: str or int
        :param status: 	1 - Вкл. / 0 - Выкл.
        :type status: str or int
        """
        if isinstance(status, bool):
            status = int(status)

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.EDIT_DISTRIBUTORS_STATUS, payload, True)

    async def get_routes(self, distributor_id: Union[str, int]):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.BE.D0.B2_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        Возвращает список всех маршрутов поставщика.


        :param distributor_id: 	Идентификатор поставщика
        :type distributor_id: str or int
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.GET_SUPPLIER_ROUTES, payload)

    async def edit_route(self,
                         route_id: Union[str, int],
                         deadline: Union[str, int] = None, deadline_replace: str = None,
                         is_deadline_replace_franch_enabled: Union[str, bool] = None,
                         deadline_max: Union[str, int] = None,
                         normal_time_start: str = None, normal_time_end: str = None,
                         normal_days_of_week: List = None,
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
                         supplier_code_enabled_list: Union[List, List, str, int] = None,
                         supplier_code_disabled_list: Union[List, List, str, int] = None,
                         normal_time_display_only: Union[int, str] = None,
                         disable_order_abnormal_time: Union[int, str] = None,
                         not_use_online_supplier_deadline: Union[int, str] = None,
                         ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B4.D0.B0.D0.BD.D0.BD.D1.8B.D1.85_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        Осуществляет обновление данных маршрута поставщика, присланных в запросе.
        При изменении данных маршрута необязательно передавать все параметры.
        Используйте в запросе только те данные, которые вы собираетесь изменить.



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
        :param not_use_online_supplier_deadline: Не использовать срок поставки online-поставщика (0 - Нет, 1 - Да)
        :type not_use_online_supplier_deadline: int or str
        :return: dict
        """
        if supplier_code_enabled_list is not None and not isinstance(supplier_code_enabled_list, list):
            supplier_code_enabled_list = [supplier_code_enabled_list]
        if supplier_code_disabled_list is not None and isinstance(supplier_code_disabled_list, list):
            supplier_code_disabled_list = [supplier_code_disabled_list]
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Distributors.UPDATE_ROUTE, payload, True)

    async def edit_route_status(self, route_id: Union[str, int], status: Union[int, bool]):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0

        Изменяет статус маршрута поставщика


        :param route_id:	Идентификатор маршрута поставщика
        :type route_id: int or str
        :param status:  Значение нового статуса (1-вкл., 0-выкл.)
        :type route_id: int or str
        :return: dict
        """
        if isinstance(status, bool):
            status = int(status)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.UPDATE_ROUTE_STATUS, payload, True)

    async def delete_route(self, route_id: Union[int, str]):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.A3.D0.B4.D0.B0.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        Удаляет маршрут поставщика.


        :param route_id:Идентификатор маршрута поставщика
        :type route_id: int or str
        :return: dict
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.DELETE_ROUTE, payload, True)

    async def connect_to_office(self, office_id: Union[str, int],
                                distributors: Union[List[Dict], Dict] = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.B4.D0.BA.D0.BB.D1.8E.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2_.D0.BA_.D0.BE.D1.84.D0.B8.D1.81.D1.83

        Подключение/отключение поставщиков к офисам
        Если параметр distributors не указан или содержит пустой список все поставщики офиса будут отключены


        :param office_id: Идентификатор офиса.
        :type office_id: int or str
        :param distributors: Массив поставщиков, если параметр не передан или содержит пустое значение - отключаются все поставщики указанного офиса.
        :type distributors List[Dict] or Dict
        :return: dict
        """
        if isinstance(distributors, dict):
            distributors = [distributors]
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.EDIT_SUPPLIER_STATUS_FOR_OFFICE, payload, True)

    async def get_office_distributors(self, office_id: Union[int, str] = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2_.D0.BE.D1.84.D0.B8.D1.81.D0.B0
        Возвращает информацию о подключенных к офису поставщиках


        :param office_id: Идентификатор офиса. Если параметр не указан то в ответе возвращаются данные по всем офисам
        :type office_id: str or int
        :return:dict
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.GET_OFFICE_SUPPLIERS, payload)

    async def pricelist_update(self, distributor_id: Union[str, int],
                               upload_file: Union[str, BufferedReader],
                               file_type_id: Union[int, str] = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.97.D0.B0.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B0_.D0.BF.D1.80.D0.B0.D0.B9.D1.81-.D0.BB.D0.B8.D1.81.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        В ПУ, в разделе "Поставщики"/"Обн."/"Конфигурация прайс-листа" предварительно настраивается конфигурация
        загружаемого прайс-листа. Специальных требований к прайс-листу нет, есть только обычные: наличие колонок
        с ценой, брендом, каталожным номером, описанием, наличием. На вкладке "Загрузка прайс-листа" может быть
        выбран любой способ загрузки


        :param distributor_id: Id поставщика
        :type distributor_id: :obj:`Union[str, int]`
        :param upload_file: путь до файла прайс-листа
        :type upload_file: :obj:`str` or :obj:`BufferedReader`
        :param file_type_id: Смысла от параметра пока нет (15.05.2022)

        :return: dict
        """

        payload = generate_file_payload(exclude=['upload_file'], **locals())
        return await self._base.request(_Methods.Admin.Distributors.UPLOAD_PRICE, payload, True)


class Catalog:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def info(self, goods_group: str, locale: str = 'ru_RU'):
        """

        :param goods_group:
        :param locale:
        :return:
        """
        payload = generate_payload(exclude=['goods_group'], **locals())
        return await self._base.request(_Methods.Admin.Catalog.INFO, payload)

    async def search(self, goods_group: str,
                     properties: Union[List[Dict[str, str]], Dict[str, str]],
                     skip: Optional[int] = None, limit: Optional[int] = None,
                     locale: Optional[str] = None):
        """

        :param goods_group:
        :param properties:
        :param skip:
        :param limit:
        :param locale:
        :return:
        """
        if isinstance(properties, dict):
            properties = [properties]
        payload = generate_payload(exclude=['goods_group', 'properties'], **locals())
        return await self._base.request(_Methods.Admin.Catalog.SEARCH, payload, True)

    async def info_batch(self, articles_catalog: Union[List[Dict[str, str]], Dict[str, str]], locale: str = 'ru_RU'):
        if isinstance(articles_catalog, dict):
            articles_catalog = [articles_catalog]
        payload = generate_payload(exclude=['articles_catalog'], **locals())
        return await self._base.request(_Methods.Admin.Catalog.INFO_BATCH, payload, True)


class UsersCatalog:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def upload(self, catalog_id: Union[str, int],
                     file: Union[str, BufferedReader],
                     delete_old_mode: int = 0,
                     default_attributes_hide: Union[str, bool] = 'false',
                     article_only: Union[str, bool] = 'false',
                     image_upload_mode: int = 0,
                     image_archive: Union[str, BufferedReader] = None):
        """

        :param catalog_id:
        :param file:
        :param delete_old_mode:
        :param default_attributes_hide:
        :param article_only:
        :param image_upload_mode:
        :param image_archive:
        :return:
        """
        if not 0 <= delete_old_mode <= 2:
            raise AbcpWrongParameterError('Параметр "delete_old_mode" должен быть в диапазоне от 0 до 2')

        if isinstance(default_attributes_hide, bool):
            default_attributes_hide = str(default_attributes_hide).lower()

        if isinstance(article_only, bool):
            article_only = str(article_only).lower()

        if image_upload_mode == 1 and image_archive is None:
            raise AbcpWrongParameterError('Не передан архив с изображениями')

        payload = generate_file_payload(exclude=['file', 'image_archive', 'catalog_id'], max_size=100, **locals())
        return await self._base.request(_Methods.Admin.UsersCatalog.UPLOAD.format(catalog_id), payload, True)


class Payment:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def token(self, number: Union[str, int]):
        """
        Получение ссылки на оплату заказа

        :param number: Онлайн-номер заказа
        :return:
        """
        if isinstance(number, str) and not number.isdigit():
            raise AbcpWrongParameterError('Параметр "number" должен быть числом')

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Payment.TOKEN, payload)

    async def top_balance_link(self, client_id: Union[str, int], amount: Union[float, int, str]):
        """

        :param client_id: Идентификатор клиента
        :param amount: Сумма пополнения баланса
        :return:
        """
        if isinstance(client_id, str) and not client_id.isdigit():
            raise AbcpWrongParameterError('Параметр "client_id" должен быть числом')
        if isinstance(amount, str) and not amount.isdigit():
            raise AbcpWrongParameterError('Параметр "amount" должен быть числом')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Payment.TOP_BALANCE, payload)
