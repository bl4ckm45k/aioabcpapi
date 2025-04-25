#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from io import BufferedReader
from typing import Dict, List

from ..api import _Methods
from ..base import BaseAbcp
from ..exceptions import AbcpAPIError, AbcpParameterRequired, AbcpWrongParameterError
from ..utils.fields_checker import check_limit, process_cp_dates, validate_numeric_params, ensure_list_params, \
    convert_bool_params, convert_bool_params_to_str
from ..utils.payload import generate_payload, generate_payload_filter, generate_payload_payments, \
    generate_payload_online_order, generate_file_payload


class Orders:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @check_limit
    @process_cp_dates(
        'date_created_start', 'date_created_end',
        'date_updated_start', 'date_updated_end')
    @ensure_list_params('status_code', 'numbers', 'internal_numbers')
    async def get_orders_list(
            self,
            date_created_start: str | datetime = None,
            date_created_end: str | datetime = None,
            date_updated_start: str | datetime = None,
            date_updated_end: str | datetime = None,
            numbers: str | int | List = None,
            internal_numbers: List | None = None,
            status_code: str | int | List = None,
            office_id: str | int = None,
            distributor_order_id: str | int = None,
            is_canceled: str | int = None,
            distributor_id: str | int | List = None,
            user_id: str | int = None,
            with_deleted: str | bool = None,
            format: str | None = None,
            limit: int | None = None,
            skip: int | None = None,
            desc: bool | None = None

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
        :type status_code: str | int | List
        :param office_id: Идентификатор офиса (в ответе по параметру могут быть отфильтрованы заказы где этот офис выбран как самовывоз или если это офис клиента или если менеджер клиента, сделавшего заказ, относится к данному офису)
        :type office_id: int or str
        :param distributor_order_id: Идентификатор заказа у поставщика. В результате вернутся все заказы которые были отправлены поставщику под этим номером.
        :type distributor_order_id: int or str
        :param is_canceled: Флаг "Запрос на удаление позиции". 0 - запрос не был отправлен, 1 - запрос отправлен, 2 - запрос отклонен менеджером.
        :type is_canceled: int or str
        :param distributor_id: Идентификатор (один или массив идентификаторов) поставщика. В результате вернутся все заказы, содержащие хотя бы одну позицию от указанного поставщика.
        :type distributor_id: str | int | List
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
        if isinstance(format, str) and format not in ["additional", "short", "count", "status_only", "p"]:
            raise AbcpWrongParameterError(
                "format",
                format,
                'должен принимать одно из значений ["additional", "short", "count", "status_only", "p"]')

        if isinstance(user_id, str) and not user_id.isdigit():
            raise AbcpAPIError(f'Параметр user_id должен быть числом')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Orders.GET_ORDERS_LIST, payload)

    @validate_numeric_params('number', 'internal_number')
    async def get_order(
            self,
            number: str | int = None,
            internal_number: str | int = None,
            with_deleted: str | bool = None,
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
            position_id: str | int

    ):
        """Принимает в качестве параметра id позиции заказа. Возвращает информацию об истории изменений статуса позиции заказа.

        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B8.D1.81.D1.82.D0.BE.D1.80.D0.B8.D0.B8_.D0.B8.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B9_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0


        :param position_id: Номер заказа int или str
        :type position_id int or str


        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Orders.STATUS_HISTORY, payload)

    @process_cp_dates('date', 'shipment_date')
    @ensure_list_params('positions')
    async def create_or_edit_order(
            self,
            number: str | int = None,
            internal_number: str | int = None,
            user_id: str | int = None,
            date: str | datetime = None,
            comment: str = None,
            order_positions: List[Dict] | Dict = None,
            delivery_type_id: str | int = None,
            delivery_office_id: str | int = None,
            basket_id: str | int = None,
            guest_order_name: str = None,
            guest_order_mobile: str = None,
            guest_order_email: str = None,
            shipment_date: str | datetime = None,
            delivery_cost: str | int | float = None,
            delivery_address_id: str | int = None,
            delivery_address: str = None,
            manager_id: str | int = None,
            client_order_number: str = None,
            note: str = None,
            del_note: str | int = None

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

    @ensure_list_params('position_ids')
    async def get_online_order_params(
            self,
            position_ids: List | str | int

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
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Orders.ONLINE_ORDER, payload)

    @ensure_list_params('positions', 'order_params')
    async def send_online_order(
            self,
            order_params: List[Dict] | Dict,
            positions: List[Dict] | Dict,
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D1.82.D0.BF.D1.80.D0.B0.D0.B2.D0.BA.D0.B0_online-.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D1.83

        :param order_params: Массив параметров заказа, который нужно сформировать на основе операции "Получение параметров для отправки online-заказа поставщику". Если у поставщика нет параметров заказа, то параметр orderParams необязательный.
        :type order_params: List of dict example: [{'shipmentAddress': 77333, 'comment': 'Мой коментарий', 'deliveryType': 3, 'contactName': 'Иванов Иван'}]
        :param positions: Массив данных с позициями заказов
        d = await api.cp.admin.get_online_order_params(id=222)
        order_params={d['orderParams'][0]['fieldName']: d['orderParams'][0]['enum'][2]['value']}, positions={'id': 263266039, 'comment': 'тест'}
        :type positions: List of ids, str or int
        """

        payload = generate_payload_online_order(**locals())

        return await self._base.request(_Methods.Admin.Orders.ONLINE_ORDER, payload, True)


class Finance:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @validate_numeric_params('user_id')
    async def update_balance(
            self,
            user_id: str | int,
            balance: str | int | float,
            in_stop_list: str | bool = None
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B1.D0.B0.D0.BD.D0.B0.D0.BD.D1.81.D0.B0_.D0.BA.D0.BB.D0.B8.D0.B5.D0.BD.D1.82.D0.B0
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
            user_id: str | int,
            credit_limit: str | int | float

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
            user_id: str | int,
            balance: str | int | float = None,
            credit_limit: float = None,
            in_stop_list: str | bool = None,
            pay_delay: str | int = None,
            overdue_saldo: str | int | float = None
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

    @process_cp_dates('create_date_time_start', 'create_date_time_end')
    async def get_payments_info(
            self,
            user_id: str | int = None,
            payment_number: str = None,
            create_date_time_start: str | datetime = None,
            create_date_time_end: str | datetime = None
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

        if all(x is None for x in [user_id, payment_number, create_date_time_start, create_date_time_end]):
            raise AbcpAPIError('Недостаточно параметров')
        if payment_number is None and any(x is None for x in [create_date_time_start, create_date_time_end]):
            raise AbcpAPIError('Недостаточно параметров')
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Finance.GET_PAYMENTS, payload)

    @process_cp_dates('date_time_start', 'date_time_end')
    @ensure_list_params('payment_numbers', 'order_ids')
    async def get_payment_links(
            self,
            payment_numbers: List | str | int = None,
            order_ids: List | str | int = None,
            user_id: str | int = None,
            date_time_start: str | datetime = None,
            date_time_end: str | datetime = None,
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

        if all(x is None for x in [user_id, date_time_start, date_time_end]):
            if any(y is not None for y in [payment_numbers, order_ids]):
                pass
            else:
                raise AbcpParameterRequired(
                    f'Недостаточно параметров, укажите user_id, date_time_start, date_time_end')
        payload = generate_payload(exclude=['date_time_start', 'date_time_end'], **locals())

        return await self._base.request(_Methods.Admin.Finance.GET_PAYMENTS_LINKS, payload)

    @process_cp_dates('date_start', 'date_end')
    @ensure_list_params('customer_ids', 'status_ids', 'order_ids')
    async def get_online_payments(
            self,
            date_start: str | datetime = None,
            date_end: str | datetime = None,
            customer_ids: List | int = None,
            payment_method_id: str | int = None,
            status_ids: List | str | int = None,
            order_ids: List | str | int = None
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

        payload = generate_payload_filter(**locals())

        return await self._base.request(_Methods.Admin.Finance.GET_PAYMENTS_ONLINE, payload)

    @convert_bool_params('link_payments')
    @ensure_list_params('payments')
    async def add_multiple_payments(
            self,
            payments: List[Dict] | Dict = None,
            link_payments: int | bool = 0
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.94.D0.BE.D0.B1.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82
        Добавляет платежи клиентам. Возвращает массив добавленных платежей.


        :param payments: Массив с оплатами
        :type payments: List[Dict] | Dict
        :param link_payments: Идентификатор платежной системы. Получить можно из cp/users/profiles или в панели управления.
        :type link_payments: str or int
        """
        payload = generate_payload_payments(single=False, **locals())

        return await self._base.request(_Methods.Admin.Finance.ADD_PAYMENTS, payload, True)

    @convert_bool_params('link_payments')
    @process_cp_dates('create_date_time')
    async def add_single_payment(
            self,
            user_id: int,
            payment_type_id: int,
            amount: int | float,
            create_date_time: str | datetime = None,
            payment_number: str | int = None,
            comment: str | None = None,
            editor_id: str | int = None,
            link_payments: int | bool = False
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

    @validate_numeric_params('payment_id', 'order_id', 'amount')
    async def link_existing_payment(
            self,
            payment_id: str | int,
            order_id: str | int,
            amount: str | int | float
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

        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Finance.LINK_EXISTING_PLAYMENT, payload, True)

    @validate_numeric_params('refund_payment_id', 'refund_amount')
    async def refund_payment(
            self,
            refund_payment_id: str | int,
            refund_amount: str | int | float
    ):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D1.8F_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BB.D0.B0.D1.82.D0.B5.D0.B6.D0.B0
        Позволяет осуществлять возврат ранее созданного платежа


        :param refund_payment_id: id платежа.
        :type refund_payment_id: int or str
        :param refund_amount: Сумма возврата.
        :type refund_amount: int or str or float
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Finance.REFUND_PAYMENT, payload, True)

    @convert_bool_params('delete_link')
    async def delete_payment(self, payment_id: int, delete_link: int | bool = 0):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Finance.DELETE_PAYMENT, payload, True)

    @process_cp_dates('date_created_start', 'date_created_end')
    async def get_receipts(
            self,
            shop_id: str | int = None,
            queue_id: str | int = None,
            date_created_start: str | datetime = None,
            date_created_end: str | datetime = None,
            calculation_method: str | int = None,
            print_paper_check: str | int = None,
            vat: str | int = None,
            calculation_subject: str | int = None,
            payment_type: str | int = None,
            type: str | int = None,
            tax_system: str | int = None,
            intent: str | int = None,
            fiscalization: str | int = None,
            employee_id: str | int = None,
            client_id: str | int = None,
            start: str | int = None,
            rows_on_page: str | int = None,
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
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Finance.GET_RECEIPTS, payload)

    async def get_payments_methods(self, only_enabled: str | bool = None,
                                   only_disabled: str | bool = None,
                                   payment_method_id: str | int = None):
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

    @process_cp_dates('date_registred_start', 'date_registred_end',
                      'date_updated_start', 'date_updated_end')
    @ensure_list_params('customers_ids')
    async def get_users(
            self,
            date_registred_start: str | datetime = None,
            date_registred_end: str | datetime = None,
            date_updated_start: str | datetime = None,
            date_updated_end: str | datetime = None,
            state: str | int = None,
            customer_status: str | int = None,
            customers_ids: List | str | int = None,
            market_type: str | int = None,
            phone: str | int = None,
            enable_sms: str | bool = None,
            email: str = None,
            safe_mode: str | int = None,
            format: str = None,
            limit: int | None = None,
            skip: int | None = None,
            desc: str | bool = 'false'
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

        if isinstance(format, str) and format != 'p':
            raise AbcpWrongParameterError("format", format, 'can only take the value "p" or None')
        if isinstance(enable_sms, str) and (enable_sms != 'true' and enable_sms != 'false'):
            raise AbcpAPIError('Параметр "enable_sms" должен быть булевым значением, либо строкой "true" или "false"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.GET_USERS_LIST, payload)

    @convert_bool_params('pickup_state')
    async def create(
            self,
            market_type: str | int,
            name: str, password: str,
            mobile: str | int,
            filial_id: str | int = None,
            second_name: str = None, surname: str = None,
            birth_date: str | datetime = None,
            member_of_club: str = None, office: str | int = None,
            email: str = None, icq: str = None,
            skype: str = None,
            region_id: str = None, city: str = None,
            organization_name: str = None, business: str | int = None,
            organization_form: str = None, organization_official_name: str = None,
            inn: str | int = None, kpp: str | int = None,
            ogrn: str | int = None, organization_official_address: str = None,
            bank_name: str = None, bik: str | int = None,
            correspondent_account: str | int = None, organization_account: str | int = None,
            delivery_address: str = None, comment: str = None, profile_id: str = None,
            pickup_state: int | bool = None
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
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.CREATE_USER, payload, True)

    async def get_profiles(
            self,
            profile_id: str | int = None,
            skip: int | None = None,
            limit: int | None = None,
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
            raise AbcpWrongParameterError(
                "format",
                format,
                'parameter can take values "brands" or "distributors"')
        del format_params_check
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.GET_PROFILES, payload)

    @ensure_list_params('matrix_price_ups', 'distributors_price_ups')
    async def edit_profile(
            self,
            profile_id: str | int,
            code: str | int = None,
            name: str = None,
            comment: str = None,
            price_up: str | int = None,
            payment_methods: str = None,
            matrix_price_ups: List[Dict] | Dict = None,
            distributors_price_ups: List[Dict] | Dict = None,

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
        payload = generate_payload(exclude=['matrix_price_ups', 'distributors_price_ups'], **locals())
        return await self._base.request(_Methods.Admin.Users.EDIT_PROFILE, payload, True)

    @convert_bool_params('pickup_state')
    async def edit(
            self,
            user_id: str | int, business: str | int = None,
            email: str = None, name: str = None, second_name: str = None,
            surname: str = None, password: str = None,
            birth_date: str | datetime = None, city: str = None,
            mobile: str | int = None, icq: str = None,
            skype: str = None, enable_sms: str | bool = None,
            enable_whatsapp: str | bool = None,
            state: str | int = None,
            profile_id: str | int = None, organization_name: str = None,
            organization_form: str = None, organization_official_name: str = None,
            inn: str | int = None, kpp: str | int = None, ogrn: str | int = None,
            bank_name: str = None, bik: str | int = None,
            correspondent_account: str | int = None, organization_account: str | int = None,
            delivery_address: List[Dict] | Dict = None, baskets: List[Dict] | Dict = None,
            baskets_delivery_address: List[Dict] | Dict = None, comment: str = None,
            manager_comment: str = None, manager_id: str | int = None,
            user_code: str | int = None, client_service_employee_id: str | int = None,
            client_service_employee2_id: str | int = None, client_service_employee3_id: str | int = None,
            client_service_employee4_id: str | int = None, office: List[Dict] | Dict = None,
            info: str = None, safe_mode: str | int = None,
            pickup_state: int | bool = None,

    ):

        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B4.D0.B0.D0.BD.D0.BD.D1.8B.D1.85_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.B6.D1.8F
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
        :param enable_whatsapp: Производится ли отправка Whatsapp клиенту
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
        if isinstance(enable_sms, str) and (enable_sms != 'true' and enable_sms != 'false'):
            raise AbcpAPIError('Параметр "enable_sms" должен быть булевым значением, либо строкой "true" или "false"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.EDIT_USER, payload, True)

    async def get_user_shipment_address(self, user_id: str | int):
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
        return await self._base.request(f"{_Methods.Admin.Users.GET_USER_SHIPMENT_ADDRESS_ZONE}{id}")

    @ensure_list_params('zones')
    async def update_shipment_zones(self, zones: List[Dict] | Dict):
        """
        Сохранение зон адресов доставки. Универсальный метод добавления и обновления зон адресов доставки.

        :param zones: Массив объектов зон адресов доставки
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.UPDATE_SHIPMENT_ZONES, payload, True)

    async def create_shipment_zone(self, name: str, desc: str, address: str, comment: str, lat: float, lng: float,
                                   radius: float):
        """
        Функция создания новой зоны доставки
        :param name: название зоны
        :param desc: описание зоны
        :param address: адрес зоны
        :param comment: дополнительный комментарий
        :param lat: координата lat зоны доставки, число с плавающей точкой
        :param lng: координата lng зоны доставки, число с плавающей точкой
        :param radius: координата radius зоны доставки, число с плавающей точкой
        :return: идентификатор id новой зоны доставки
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.CREATE_SHIPMENT_ZONE, payload, post=True,
                                        json=True)

    async def update_shipment_zone(self, shipment_zone_id: str, name: str = None, desc: str = None, address: str = None,
                                   comment: str = None, lat: float = None, lng: float = None, radius: float = None):
        """
        Функция изменения существующей зоны доставки
        :param shipment_zone_id: id зоны доставки
        :param name: название зоны
        :param desc: описание зоны
        :param address: адрес зоны
        :param comment: дополнительный комментарий
        :param lat: координата lat зоны доставки, число с плавающей точкой
        :param lng: координата lng зоны доставки, число с плавающей точкой
        :param radius: координата radius зоны доставки, число с плавающей точкой
        :return: ассоциотивный массив с обновленными полями зоны доставки
        """
        _method = _Methods.Admin.Users.UPDATE_SHIPMENT_ZONE.format(id=shipment_zone_id)
        payload = generate_payload(**locals())
        return await self._base.request(_method, payload, post=True, json=True)

    async def delete_shipment_zone(self, id: int):
        return await self._base.request(f"{_Methods.Admin.Users.DELETE_SHIPMENT_ZONE}{id}", None, True)

    @process_cp_dates('date_updated_start', 'date_updated_end')
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
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.GET_USERS_CARS, payload)

    @ensure_list_params('user_ids')
    async def get_sms_settings(self, user_ids: List | int | str):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Users.SMS_SETTINGS, payload)


class Staff:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D0.BE.D1.82.D1.83.D0.BD.D0.B8.D0.BA.D0.BE.D0.B2
        Возвращает список менеджеров.
        """
        return await self._base.request(_Methods.Admin.Staff.GET_STAFF)

    @validate_numeric_params('sip')
    async def update_manager(self, id: int, type_id: int = None,
                             first_name: str = None, last_name: str = None,
                             email: str = None, phone: str = None, mobile: str = None,
                             sip: str | int = None, comment: str = None, boss_id: int = None, office_id: int = None):
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

    @convert_bool_params('distributors4mc')
    async def get(self, distributors4mc: str | int | bool = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2
        Возвращает список всех поставщиков, подключенных в ПУ/Поставщики.


        :param distributors4mc: При передаче "1" возвращает дополнительно поставщиков 4mycar"
        :type distributors4mc: str or int
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.GET_DISTRIBUTORS_LIST, payload)

    @convert_bool_params('status')
    async def edit_status(self, distributor_id: str | int, status: int | bool):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        Изменение статуса поставщика


        :param distributor_id: 	Id поставщика
        :type distributor_id: str or int
        :param status: 	1 - Вкл. / 0 - Выкл.
        :type status: str or int
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.EDIT_DISTRIBUTORS_STATUS, payload, True)

    @validate_numeric_params('distributor_id')
    async def get_routes(self, distributor_id: str | int):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.BE.D0.B2_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        Возвращает список всех маршрутов поставщика.


        :param distributor_id: 	Идентификатор поставщика
        :type distributor_id: str or int
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.GET_SUPPLIER_ROUTES, payload)

    @ensure_list_params('supplier_code_enabled_list', 'supplier_code_disabled_list')
    async def edit_route(self,
                         route_id: str | int,
                         deadline: str | int = None, deadline_replace: str = None,
                         is_deadline_replace_franch_enabled: str | bool = None,
                         deadline_max: str | int = None,
                         normal_time_start: str = None, normal_time_end: str = None,
                         normal_days_of_week: List = None,
                         abnormal_deadline: str | int = None,
                         abnormal_deadline_max: str | int = None,
                         p1: str | int = None, p2: str | int = None,
                         price_per_kg: str | int = None,
                         price_up_added: str | int = None,
                         c1: str | int = None,
                         price_up_min: str | int = None, price_up_max: str | int = None,
                         primary_price_up_to_contractor: str | int = None,
                         delivery_probability: str | int = None,
                         description: str = None,
                         enable_color: str | bool = None, color: str = None,
                         is_abnormal_color_enabled: str | bool = None, abnormal_color: str = None,
                         no_return: str | bool = None,
                         supplier_code_enabled_list: List | str | int = None,
                         supplier_code_disabled_list: List | str | int = None,
                         normal_time_display_only: str | int = None,
                         disable_order_abnormal_time: str | int = None,
                         not_use_online_supplier_deadline: str | int = None,
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
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Admin.Distributors.UPDATE_ROUTE, payload, True)

    @convert_bool_params('status')
    async def edit_route_status(self, route_id: str | int, status: int | bool):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0

        Изменяет статус маршрута поставщика


        :param route_id:	Идентификатор маршрута поставщика
        :type route_id: int or str
        :param status:  Значение нового статуса (1-вкл., 0-выкл.)
        :type route_id: int or str
        :return: dict
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.UPDATE_ROUTE_STATUS, payload, True)

    async def delete_route(self, route_id: str | int):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.A3.D0.B4.D0.B0.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BC.D0.B0.D1.80.D1.88.D1.80.D1.83.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        Удаляет маршрут поставщика.


        :param route_id:Идентификатор маршрута поставщика
        :type route_id: int or str
        :return: dict
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.DELETE_ROUTE, payload, True)

    @ensure_list_params('distributors')
    async def connect_to_office(self, office_id: str | int,
                                distributors: List[Dict] | Dict = None):
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
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.EDIT_SUPPLIER_STATUS_FOR_OFFICE, payload, True)

    async def get_office_distributors(self, office_id: str | int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.BE.D0.B2_.D0.BE.D1.84.D0.B8.D1.81.D0.B0
        Возвращает информацию о подключенных к офису поставщиках


        :param office_id: Идентификатор офиса. Если параметр не указан то в ответе возвращаются данные по всем офисам
        :type office_id: str or int
        :return:dict
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Distributors.GET_OFFICE_SUPPLIERS, payload)

    async def pricelist_update(self, distributor_id: str | int,
                               upload_file: str | BufferedReader,
                               file_type_id: str | int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Admin#.D0.97.D0.B0.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B0_.D0.BF.D1.80.D0.B0.D0.B9.D1.81-.D0.BB.D0.B8.D1.81.D1.82.D0.B0_.D0.BF.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D1.89.D0.B8.D0.BA.D0.B0
        В ПУ, в разделе "Поставщики"/"Обн."/"Конфигурация прайс-листа" предварительно настраивается конфигурация
        загружаемого прайс-листа. Специальных требований к прайс-листу нет, есть только обычные: наличие колонок
        с ценой, брендом, каталожным номером, описанием, наличием. На вкладке "Загрузка прайс-листа" может быть
        выбран любой способ загрузки


        :param distributor_id: Id поставщика
        :type distributor_id: :obj:`str | int`
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

    @ensure_list_params('properties')
    async def search(self, goods_group: str,
                     properties: List[Dict[str, str]] | Dict[str, str],
                     skip: int | None = None, limit: int | None = None,
                     locale: str | None = None):
        """

        :param goods_group:
        :param properties:
        :param skip:
        :param limit:
        :param locale:
        :return:
        """
        payload = generate_payload(exclude=['goods_group', 'properties'], **locals())
        return await self._base.request(_Methods.Admin.Catalog.SEARCH, payload, True)

    @ensure_list_params('articles_catalog')
    async def info_batch(self, articles_catalog: List[Dict[str, str]] | Dict[str, str], locale: str = 'ru_RU'):
        payload = generate_payload(exclude=['articles_catalog'], **locals())
        return await self._base.request(_Methods.Admin.Catalog.INFO_BATCH, payload, True)


class UsersCatalog:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @convert_bool_params_to_str('default_attributes_hide', 'article_only')
    async def upload(self, catalog_id: str | int,
                     file: str | BufferedReader,
                     delete_old_mode: int = 0,
                     default_attributes_hide: str | bool = 'false',
                     article_only: str | bool = 'false',
                     image_upload_mode: int = 0,
                     image_archive: str | BufferedReader = None):
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
            raise AbcpWrongParameterError(
                "delete_old_mode", delete_old_mode, 'Параметр должен быть в диапазоне от 0 до 2')

        if image_upload_mode == 1 and image_archive is None:
            raise AbcpWrongParameterError(
                "image_archive", image_archive, 'Не передан архив с изображениями')

        payload = generate_file_payload(exclude=['file', 'image_archive', 'catalog_id'], max_size=100, **locals())
        return await self._base.request(f"{_Methods.Admin.UsersCatalog.UPLOAD}{catalog_id}", payload, True)


class Payment:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def token(self, number: str | int):
        """
        Получение ссылки на оплату заказа

        :param number: Онлайн-номер заказа
        :return:
        """
        if isinstance(number, str) and not number.isdigit():
            raise AbcpWrongParameterError("number", number, 'Параметр должен быть числом')

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Payment.TOKEN, payload)

    async def top_balance_link(self, client_id: str | int, amount: str | int | float):
        """

        :param client_id: Идентификатор клиента
        :param amount: Сумма пополнения баланса
        :return:
        """
        if isinstance(client_id, str) and not client_id.isdigit():
            raise AbcpWrongParameterError("client_id", client_id, 'Параметр должен быть числом')
        if isinstance(amount, str) and not amount.isdigit():
            raise AbcpWrongParameterError("amount", amount, 'Параметр должен быть числом')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Admin.Payment.TOP_BALANCE, payload)


class AdminApi:
    def __init__(self, base: BaseAbcp):
        """
        Класс содержит методы административного интерфейса

        https://www.abcp.ru/wiki/API.ABCP.Admin
        """
        if not isinstance(base, BaseAbcp):
            raise AbcpWrongParameterError("base", base, "BaseAbcp instance")
        self._base = base
        self._orders: Orders | None = None
        self._finance: Finance | None = None
        self._users: Users | None = None
        self._staff: Staff | None = None
        self._statuses: Statuses | None = None
        self._distributors: Distributors | None = None
        self._catalog: Catalog | None = None
        self._articles: Articles | None = None
        self._users_catalog: UsersCatalog | None = None
        self._payment: Payment | None = None

    @property
    def orders(self) -> Orders:
        if self._orders is None:
            self._orders = Orders(self._base)
        return self._orders

    @property
    def finance(self) -> Finance:
        if self._finance is None:
            self._finance = Finance(self._base)
        return self._finance

    @property
    def users(self) -> Users:
        if self._users is None:
            self._users = Users(self._base)
        return self._users

    @property
    def staff(self) -> Staff:
        if self._staff is None:
            self._staff = Staff(self._base)
        return self._staff

    @property
    def statuses(self) -> Statuses:
        if self._statuses is None:
            self._statuses = Statuses(self._base)
        return self._statuses

    @property
    def distributors(self) -> Distributors:
        if self._distributors is None:
            self._distributors = Distributors(self._base)
        return self._distributors

    @property
    def catalog(self) -> Catalog:
        if self._catalog is None:
            self._catalog = Catalog(self._base)
        return self._catalog

    @property
    def articles(self) -> Articles:
        if self._articles is None:
            self._articles = Articles(self._base)
        return self._articles

    @property
    def users_catalog(self) -> UsersCatalog:
        if self._users_catalog is None:
            self._users_catalog = UsersCatalog(self._base)
        return self._users_catalog

    @property
    def payment(self) -> Payment:
        if self._payment is None:
            self._payment = Payment(self._base)
        return self._payment
