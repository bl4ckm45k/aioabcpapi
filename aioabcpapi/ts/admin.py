import base64
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Union, List, Dict, Optional

import pytz
from pyrfc3339 import generate

from ..api import _Methods
from ..base import BaseAbcp
from ..exceptions import AbcpWrongParameterError, AbcpParameterRequired
from ..utils.fields_checker import check_fields
from ..utils.payload import generate_payload


class TsAdminApi:
    def __init__(self, base: BaseAbcp):
        """
        Класс содержит методы административного интерфейса

        https://www.abcp.ru/wiki/API.TS.Admin
        """
        self._base = base
        self.order_pickings = OrderPickings(base)
        self.customer_complaints = CustomerComplaints(base)
        self.supplier_returns = SupplierReturns(base)
        self.distributor_owners = DistributorOwners(base)
        self.orders = Orders(base)
        self.cart = Cart(base)
        self.positions = Positions(base)
        self.good_receipts = GoodReceipts(base)
        self.tags = Tags(base)
        self.tags_relationships = TagsRelationships(base)
        self.payments = Payments(base)
        self.payment_methods = PaymentMethods(base)
        self.agrements = Agreements(base)
        self.legal_persons = LegalPersons(base)


class SupplierReturns:

    def __init__(self, base: BaseAbcp):
        self._base = base
        self.operations = SupplierReturnsOperations(base)
        self.positions = SupplierReturnsPositions(base)
        self.positions_attr = SupplierReturnsPositionsAttr(base)


class SupplierReturnsOperations:
    def __init__(self, base: BaseAbcp):
        self._base = base

    class _FieldsChecker:
        list_fields = ["goodsReceipt", "agreement", "tags", ]

    async def get_list(self, creator_id: int, supplier_id: int,
                       goods_receipt_id: int,
                       agreement_ids: Union[List[int], int],
                       tag_ids: Union[List[int], int],
                       sbis_statuses: Union[List[str], str],
                       date_start: Union[datetime, str],
                       date_end: Union[datetime, str],
                       skip: int, limit: int, fields: Union[List, str] = None
                       ):
        if isinstance(agreement_ids, list):
            agreement_ids = ','.join(map(str, tag_ids))
        if isinstance(tag_ids, list):
            tag_ids = ','.join(map(str, tag_ids))
        if isinstance(sbis_statuses, list):
            sbis_statuses = ','.join(map(str, tag_ids))
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.list_fields)

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.LIST, payload)

    async def get_sum(self, creator_id: int, supplier_id: int,
                      goods_receipt_id: int,
                      agreement_ids: Union[List[int], int],
                      tag_ids: Union[List[int], int],
                      sbis_statuses: Union[List[str], str],
                      date_start: Union[datetime, str], date_end: Union[datetime, str],
                      skip: int = None, limit: int = None
                      ):
        if isinstance(agreement_ids, list):
            agreement_ids = ','.join(map(str, agreement_ids))
        if isinstance(tag_ids, list):
            tag_ids = ','.join(map(str, tag_ids))
        if isinstance(sbis_statuses, list):
            sbis_statuses = ','.join(map(str, sbis_statuses))
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.SUM, payload)

    async def get(self, id: int):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.GET, payload)

    async def create(self, creator_id: int, supplier_id: int,
                     goods_receipt_id: int, agreement_id: int):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.CREATE, payload, True)

    async def update(self, id: int, number: str = None, fields: Union[List, str] = None):
        if isinstance(fields, list):
            fields = check_fields(fields, self._FieldsChecker.list_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.UPDATE, payload, True)

    async def delete(self, id: int):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.DELETE, payload, True)


class SupplierReturnsPositions:
    def __init__(self, base: BaseAbcp):
        self._base = base

    class _FieldsChecker:
        list_fields = ["item", "location", "operationInfo", "tags",
                       "goodsReceiptPos", "availableQuantity", "customerComplaintPos"]

    async def get_list(self, op_id: int = None, status: int = None, type: int = None,
                       goods_receipt_pos_ids: Union[List[str], str] = None,
                       item_ids: Union[List[str], str] = None,
                       supplier_id: str = None,
                       goods_receipt_ids: Union[List[str], str] = None,
                       date_start: Union[datetime, str] = None,
                       date_end: Union[datetime, str] = None,
                       skip: int = None,
                       limit: int = None,
                       fields: Union[List[str], str] = None
                       ):
        if isinstance(goods_receipt_pos_ids, list):
            goods_receipt_pos_ids = ','.join(map(str, goods_receipt_pos_ids))
        if isinstance(item_ids, list):
            item_ids = ','.join(map(str, item_ids))
        if isinstance(goods_receipt_ids, list):
            goods_receipt_ids = ','.join(map(str, goods_receipt_ids))
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(fields, list):
            fields = check_fields(fields, self._FieldsChecker.list_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.LIST, payload)

    async def get_sum(self, op_id: int = None, status: int = None, type: int = None,
                      goods_receipt_pos_ids: Union[List[str], str] = None,
                      item_ids: Union[List[str], str] = None,
                      supplier_id: str = None,
                      goods_receipt_ids: Union[List[str], str] = None,
                      date_start: Union[datetime, str] = None,
                      date_end: Union[datetime, str] = None,
                      skip: int = None,
                      limit: int = None,
                      fields: Union[List[str], str] = None):
        if isinstance(goods_receipt_pos_ids, list):
            goods_receipt_pos_ids = ','.join(map(str, goods_receipt_pos_ids))
        if isinstance(item_ids, list):
            item_ids = ','.join(map(str, item_ids))
        if isinstance(goods_receipt_ids, list):
            goods_receipt_ids = ','.join(map(str, goods_receipt_ids))
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(fields, list):
            fields = check_fields(fields, self._FieldsChecker.list_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.SUM, payload)

    async def status(self):
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.STATUS)

    async def get(self, id: int):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.GET, payload)

    async def create_multiple(self, op_id: int, poses_data: Union[List[Dict], Dict]):
        # TODO: PREPARE poses_data maybe we can use dataclass constructor
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.CREATE_MULTIPLE, payload, True)

    async def split(self, id: int, quantity: Union[int, float],
                    fields: Union[List[str], str] = None):
        if isinstance(fields, list):
            fields = check_fields(fields, self._FieldsChecker.list_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.SPLIT, payload, True)

    async def update(self, id: int, type: int = None, loc_id: int = None, quantity: int = None,
                     comment: str = None, fields: Union[List[str], str] = None):
        if isinstance(fields, list):
            fields = check_fields(fields, self._FieldsChecker.list_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.UPDATE, payload, True)

    async def change_status(self, id: int, status: int, fields: Union[List[str], str] = None):
        if isinstance(fields, list):
            fields = check_fields(fields, self._FieldsChecker.list_fields)

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.CHANGE_STATUS, payload, True)


class SupplierReturnsPositionsAttr:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def create(self, id: int, attr: Dict):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.PositionsAttr.CREATE, payload, True)

    async def update(self, id: int, old_name: str, new_name, description: str):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.PositionsAttr.UPDATE, payload, True)

    async def delete(self, id: int, name: str):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.PositionsAttr.DELETE, payload, True)


class OrderPickings:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def fast_get_out(self, client_id: Union[str, int], supplier_id: Union[str, int],
                           positions: Union[List[Dict], Dict], distributor_id: Union[str, int] = None,
                           route_id: Union[str, int] = None, location_id: Union[str, int] = None,
                           order_picking_reseller_data: Dict = None,
                           number: Union[str, int] = None, date: Union[datetime, str] = None,
                           ):
        """
        Операция быстрого создания заказа, приёмки, расхода

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9E.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D1.8F_.D0.B1.D1.8B.D1.81.D1.82.D1.80.D0.BE.D0.B3.D0.BE_.D1.81.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D1.8F_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0.2C_.D0.BF.D1.80.D0.B8.D1.91.D0.BC.D0.BA.D0.B8.2C_.D1.80.D0.B0.D1.81.D1.85.D0.BE.D0.B4.D0.B0


        :param client_id: Идентификатор клиента.
        :param supplier_id: Идентификатор поставщика.
        :param positions: Массив объектов позиций отгрузки. :obj:`dict` или :obj:`List[Dict]`
        :param distributor_id: Идентификатор прайс-листа.
        :param route_id: Идентификатор маршрута.
        :param location_id: Идентификатор места хранения.
        :param order_picking_reseller_data: Дополнительная информация в формате json, которая будет сохранена в операцию отгрузки
        :param number: Номер отгрузки, если пустой, то будет заполнен автоматически
        :param date: Дата отгрузки, если пустая, то будет заполнена автоматически. `str` в формате RFC3339 или datetime object
        :return: None
        """
        if isinstance(date, datetime):
            date = generate(date.replace(tzinfo=pytz.utc))
        if isinstance(positions, dict):
            positions = [positions]
        payload = generate_payload(exclude=['positions'], **locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.FAST_GET_OUT, payload, True)

    async def get(self, id: Union[int, str] = None, client_id: Union[int, str] = None, limit: int = None,
                  skip: int = None,
                  output: str = None, auto: str = None, creator_id: Union[int, str] = None,
                  worker_id: Union[int, str] = None,
                  agreement_id: Union[int, str] = None, statuses: Union[List, str, int] = None,
                  number: int = None, date_start: Union[str, datetime] = None, date_end: Union[str, datetime] = None,
                  co_old_pos_ids: Union[List, str, int] = None):
        """
        Получение списка операций отгрузка (расход)


        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BE.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D0.B9_.D0.BE.D1.82.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B0_.28.D1.80.D0.B0.D1.81.D1.85.D0.BE.D0.B4.29

        :param id: Идентификатор операции. При использовании вернётся одна операция, а не список.
        :param client_id: Идентификатор клиента.
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param skip: количество операций в ответе, которое нужно пропустить
        :param output: формат вывода, флаг 'e' - загрузка дополнительной информации (договора, места хранения, доставки, упаковки), 't' - загрузка информации о тегах, 's' - суммы по позициям, кол-во позиций
        :param auto: автоопределяемое поле (поиск по частичному номеру операции или идентификатору, если задано число)
        :param creator_id: Идентификатор сотрудника-создателя
        :param worker_id: Идентификатор сотрудника-исполнителя
        :param agreement_id: Идентификатор договора
        :param statuses: список статусов (1 - новая, 2 - сборка, 5 - готов к выдаче, 3 - завершена, 4 - аннулирована.)
        :param number: номер операций
        :param date_start: начальная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param date_end: конечная  дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param co_old_pos_ids: список идентификаторов позиций старых заказов
        :return:
        """
        # ISSUE: The "d" flag is not described in the documentation
        if isinstance(output, str) and any(x not in ["e", "t", "s", "d"] for x in output):
            raise AbcpWrongParameterError('Параметр "output" принимает флаги "e", "t", "s", "d"')
        if isinstance(limit, int) and not 1 <= limit <= 1000:
            raise AbcpWrongParameterError('Параметр "limit" должен быть в диапазоне от 1 до 1000')
        if isinstance(limit, str) and not limit.isdigit():
            raise AbcpWrongParameterError('Параметр "limit" должен быть числом')
        if statuses is not None and any(not (1 <= int(x) <= 5) for x in statuses):
            raise AbcpWrongParameterError('Параметр "statuses" принимает значения от 1 до 5')
        if isinstance(statuses, (int, str)):
            statuses = [statuses]
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(co_old_pos_ids, (int, str)):
            co_old_pos_ids = [co_old_pos_ids]
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.GET, payload, True)

    async def get_goods(self, op_id: Union[str, int], limit: int = None, skip: int = None,
                        output: str = None, product_id: Union[int, str] = None, item_id: Union[int, str] = None,
                        ignore_canceled: Union[int, bool] = None):
        """
        Получение списка позиций товаров операции отгрузки

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B9_.D1.82.D0.BE.D0.B2.D0.B0.D1.80.D0.BE.D0.B2_.D0.BE.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D1.82.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B8


        :param op_id: Идентификатор операции
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param skip: количество операций в ответе, которое нужно пропустить
        :param output: формат вывода, 'e' - загрузка дополнительной информации (справочные товары), 'o' - дополнительно вернуть инфу об операции
        :param product_id: Идентификатор товара справочника
        :param item_id:  идентификатор партии товара
        :param ignore_canceled: не возвращать позиции аннулированных операций
        :return:
        """
        if isinstance(op_id, str) and not op_id.isdigit():
            raise AbcpWrongParameterError('Параметр "op_id" должен быть числом')
        if isinstance(limit, int) and not 1 <= limit <= 1000:
            raise AbcpWrongParameterError('Параметр "limit" должен быть в диапазоне от 1 до 1000')
        if isinstance(ignore_canceled, int):
            if ignore_canceled == 0:
                ignore_canceled = None
            elif ignore_canceled != 1:
                raise AbcpWrongParameterError(
                    'В параметр "ignore_canceled" передеаются значения 1 или True, 0 или False (В данном случае можно не указывать) ')
        if isinstance(ignore_canceled, bool):
            if ignore_canceled:
                ignore_canceled = int(ignore_canceled)
            else:
                ignore_canceled = None
        if isinstance(output, str) and any(x not in ["e", "o"] for x in output):
            raise AbcpWrongParameterError(f'Параметр "output" принимает флаги "e", "o"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.GET_GOODS, payload)

    async def create_by_old_pos(self, agreement_id: Union[str, int], account_details_id: Union[str, int],
                                loc_id: Union[str, int],
                                pp_ids: Union[List, str, int], op_id: Union[int, str] = None,
                                status_id: Union[int, str] = None,
                                done_right_away: Union[int, bool] = None, output: str = None):
        """
        Создание операции отгрузки по клиентскому заказу

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.BE.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D1.82.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B8_.D0.BF.D0.BE_.D0.BA.D0.BB.D0.B8.D0.B5.D0.BD.D1.82.D1.81.D0.BA.D0.BE.D0.BC.D1.83_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D1.83

        :param op_id: Идентификатор операции для добавления позиций. Если не указан - будет создана новая операция отгрузки.
        :param agreement_id: Идентификатор договора
        :param account_details_id: Идентификатор реквизитов магазина
        :param loc_id: Идентификатор места хранения
        :param pp_ids: список идентификаторов позиций старых заказов для добавления в отгрузку
        :param status_id: 	[обязательный при указании флага doneRightAway] статус позиции заказа, в который будут переведены указанные позиции в случае успешного добавления в операцию отгрузки. При указании флага doneRightAway статус должен иметь признак списания.
        :param done_right_away: 1 - сразу завершить операцию после добавления позиций.
        :param output: расширенный формат вывода. 'e' - загрузка дополнительной информации (договора, реквизиты, клиент), 't' - загрузка информации о тегах, 's' - загрузка суммарной информации о позициях
        :return:
        """
        if isinstance(done_right_away, bool):
            done_right_away = int(done_right_away)
        if status_id is None and done_right_away == 1:
            raise AbcpParameterRequired(
                'При указании параметра done_right_away, status_id является обязательным и должен иметь признак списания')
        if isinstance(pp_ids, (int, str)):
            pp_ids = [pp_ids]
        if isinstance(output, str) and any(x not in ["e", "t", "s"] for x in output):
            raise AbcpWrongParameterError('Параметр "output" принимает флаги "e", "t", "s"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.CREATE_BY_OLD_POS, payload, True)

    async def change_status(self, id: int, operation_status_id: Union[str, int],
                            positions_status_id: Union[int, str] = None):
        """
        Изменение статуса операции отгрузка

        Source:  https://www.abcp.ru/wiki/API.TS.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BE.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D1.82.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B0

        :param id: [обязательный] идентификатор операции отгрузка.
        :param operation_status_id: [обязательный] статус в который требуется перевести отгрузку: 1 - новая, 2 - сборка, 5 - готов к выдаче, 3 - завершена, 4 - аннулирована.
        :param positions_status_id: [обязательный при смене статуса операции с 5 на 3 и с 3 на 5] идентификатор статуса в который требуется перевести связанные с отгрузкой позиции заказов. При переводе из статуса "готов к выдаче" в статус "завершена" требуется указать статус с признаком "списание товара на складе". При переводе из статуса "завершена" в статус "готов к выдаче" требуется указать статус с признаком "бронирование товара".
        :return:
        """
        if operation_status_id > 5 or operation_status_id < 1:
            raise AbcpWrongParameterError('Параметр "operation_status_id" может принимать значения от 1 до 5')
        if positions_status_id is None and operation_status_id in (3, 5):
            raise AbcpWrongParameterError(
                f'Параметр "positions_status_id" является обязательным при смене статуса операции на {operation_status_id}')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.CHANGE_STATUS, payload, True)

    async def update(self, id: int, number: Union[str, int] = None, creator_id: Union[int, str] = None,
                     worker_id: Union[int, str] = None,
                     client_id: Union[int, str] = None,
                     agreement_id: Union[int, str] = None, account_details_id: Union[int, str] = None,
                     loc_id: Union[int, str] = None,
                     reseller_data: Dict = None):
        """
        Изменение операции отгрузка

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D1.82.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B0

        :param id: Идентификатор операции отгрузки.
        :param number: номер операции
        :param creator_id: Идентификатор сотрудника-создателя
        :param worker_id: Идентификатор сотрудника-исполнителя
        :param client_id: Идентификатор клиента
        :param agreement_id: Идентификатор договора
        :param account_details_id: Идентификатор реквизитов магазина
        :param loc_id: Идентификатор места хранения
        :param reseller_data: Дополнительная информация в формате dict, которая будет сохранена в операцию отгрузки.
        :return:
        """
        payload = generate_payload(exclude=['reseller_data'], **locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.UPDATE, payload, True)

    async def delete(self, id: int):
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.DELETE_POSITION, payload, True)


class CustomerComplaints:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @dataclass
    class _FieldsChecker:
        get_fields = ["orderPicking", "agreement", "tags", "posInfo"]
        get_positions_fields = ["item", "product", "location", "orderPickingInfo", "tags", "operationInfo",
                                "supplierReturnPos"]
        update_fields = ["orderPicking", "agreement", "posInfo"]

    async def get(self, id: int = None, client_id: Union[int, str] = None, creator_id: Union[int, str] = None,
                  expert_id: Union[int, str] = None,
                  auto: Union[int, str] = None,
                  number: int = None, order_picking_id: Union[int, str] = None,
                  position_statuses: Union[List, int] = None,
                  position_type: int = None, position_auto: Union[str, int] = None,
                  date_start: Union[datetime, str] = None,
                  date_end: Union[datetime, str] = None,
                  skip: int = None, limit: int = None, fields: Union[List, str] = None):
        """
        Получение списка возвратов покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.BE.D0.B2_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param id: Идентификатор операции. При использовании вернётся одна операция, а не список.
        :param client_id: Идентификатор клиента для фильтра операций.
        :param creator_id: Идентификатор сотрудника-создателя.
        :param expert_id: Идентификатор сотрудника-эксперта.
        :param auto: Автоопределяемый параметр для поиска по операции.
        :param number: Номер операции.
        :param order_picking_id: Идентификатор операции расхода по выдаче клиенту.
        :param position_statuses: Поиск операций, которые содержат позиции в указанных статусах.
        :param position_type: поиск операций, которые содержат позиции указанного типа(1-возврат, 2-отказ, 3-брак)
        :param position_auto: автоопределяемый параметр для поиска по позициям операции.
        :param date_start:  Начальная дата диапазона поиска. `str` в формате RFC3339 или datetime object
        :param date_end: Конечная дата диапазона поиска. `str` в формате RFC3339 или datetime object
        :param skip: Количество операций в ответе, которое нужно пропустить.
        :param limit: Количество операций, которое нужно получить.
        :param fields:
        :return:
        """
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(position_type, int) and (position_type < 1 or position_type > 3):
            raise AbcpWrongParameterError('position_type parameter must be between 1 and 3')
        if isinstance(position_statuses, list):
            position_statuses = ','.join(map(str, position_statuses))
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.get_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.GET, payload)

    async def get_positions(self, op_id: Union[int, str] = None, order_picking_good_id: Union[int, str] = None,
                            order_picking_good_ids: Union[List, int] = None,
                            picking_ids: Union[List, int] = None,
                            old_co_position_ids: Union[List, int] = None,
                            client_id: Union[str, int] = None, old_item_id: Union[int, str] = None,
                            item_id: Union[int, str] = None,
                            tag_ids: Union[List, int] = None,
                            loc_id: Union[int, str] = None, status: int = None, type: int = None,
                            date_start: Union[datetime, str] = None,
                            date_end: Union[datetime, str] = None,
                            skip: int = None, limit: int = None,
                            sort: str = None, output: str = None,
                            fields: Union[List, str] = None):
        """
        Получение списка позиций операции возврата покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B9_.D0.BE.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D0.B8_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param op_id: Идентификатор операции.
        :param order_picking_good_id: Идентификатор позиции расхода по выдаче клиенту.
        :param order_picking_good_ids: Идентификаторы позиций расхода через запятую.
        :param picking_ids: Идентификаторы операции расхода.
        :param old_co_position_ids: Идентификаторы позиции заказа через запятую.
        :param client_id: Идентификатор клиента.
        :param old_item_id: Идентификатор старой партии.
        :param item_id: Числовой идентификатор партии.
        :param tag_ids: Идентификаторы тегов через запятую.
        :param loc_id: Идентификатор места хранения.
        :param status: Статус позиции. От 1 до 8
        :param type: Тип возврата (1-возврат, 2-отказ, 3-брак).
        :param date_start: Минимальная дата создания операциию. `str` в формате RFC3339 или datetime object
        :param date_end: Максимальная дата создания операции. `str` в формате RFC3339 или datetime object
        :param skip: Количество операций в ответе, которое нужно пропустить.
        :param limit: Максимальное количество позиций, которое дожно быть возвращено в ответе.
        :param sort: Как сортировать позиции: status - по статусу, createDate - по дате создания операции.
        :param output:
        :param fields:
        :return:
        """
        if isinstance(sort, str) and sort not in ('status', 'createDate'):
            raise AbcpWrongParameterError('Параметр "sort" может принимать одно из значений: "status" или "createDate"')

        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(picking_ids, list):
            picking_ids = ','.join(map(str, picking_ids))
        if isinstance(order_picking_good_ids, list):
            order_picking_good_ids = ','.join(map(str, order_picking_good_ids))
        if isinstance(old_co_position_ids, list):
            old_co_position_ids = ','.join(map(str, old_co_position_ids))
        if isinstance(tag_ids, list):
            tag_ids = ','.join(map(str, tag_ids))
        if isinstance(status, int) and not 1 <= status <= 8:
            raise AbcpWrongParameterError('Параметр "status" должен быть в диапазоне от 1 до 8')
        if isinstance(type, int) and not 1 <= type <= 3:
            raise AbcpWrongParameterError('Параметр "type" должен быть в диапазоне от 1 до 3')
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.get_positions_fields)
        payload = generate_payload(exclude=['old_item_id'], **locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.GET_POSITIONS, payload)

    async def create(self, order_picking_id: Union[str, int], positions: Union[List[Dict], Dict]):
        """
        Создание возврата покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param order_picking_id: Идентификатор операции отгрузки из которой возвращается товар
        :param positions: Список позиций.
        :return:
        """
        # Прощай маржинальность :(
        if isinstance(positions, dict):
            positions = [positions]
        payload = generate_payload(exclude=['positions'], **locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.CREATE, payload, True)

    async def create_position(self, op_id: Union[str, int], order_picking_position_id: Union[str, int], quantity: int,
                              type: int, comment: str):
        """
        Создание позиции возврата покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param op_id: Идентификатор операции возврата
        :param order_picking_position_id: Идентификатор позиции отгрузки
        :param quantity: количество к возврату
        :param type: тип возврата(1-возврат, 2-отказ, 3-брак)
        :param comment:комментарий
        :return:
        """
        if not 1 <= type <= 3:
            raise AbcpWrongParameterError('Параметр "type" может принимать значения от 1 до 3')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.CREATE_POSITION, payload, True)

    async def create_position_multiple(self, positions: Union[List[Dict], Dict],
                                       customer_complaint_id: int,
                                       customer_complaint: str,
                                       custom_complaint_file: str = None):
        with open(custom_complaint_file, "rb") as ccf:
            encoded_string = base64.b64encode(ccf.read()).decode("utf-8")
        custom_complaint_file = f"{encoded_string}"
        del ccf
        del encoded_string
        if isinstance(positions, dict):
            positions = [positions]
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.CREATE_POSITION_MULTIPLE, payload, True)

    async def update_position(self, id: int, quantity: int = None, type: int = None, comment: str = None):
        """
        Изменение позиции возврата покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param id: Идентификатор позиции возврата покупателя
        :param quantity: количество
        :param type: тип возврата
        :param comment: комментарий
        :return:
        """
        if all(x is None for x in [quantity, type, comment]):
            raise AbcpParameterRequired('Один из параметров [quantity, type, comment] должен быть указан')
        if isinstance(type, int) and not 1 <= type <= 3:
            raise AbcpWrongParameterError('Параметр "type" может принимать значения от 1 до 3')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.UPDATE_POSITION, payload, True)

    async def change_position_status(self, id: int, status: int):
        """
        Изменение статуса позиции возврата покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param id:
        :param status:
        :return:
        """
        if not (1 <= status <= 8):
            raise AbcpWrongParameterError('Параметр "status" может принимать значения от 1 до 8')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.CHANGE_STATUS_POSITION, payload, True)

    async def update(self, id: Union[str, int], number: int = None, expert_id: Union[int, str] = None,
                     custom_complaint_file: str = '',
                     fields: Union[List, str] = None):
        """

        :param id: [обязательный] идентификатор операции возврата покупателя
        :param number: [обязательный если не задан expert_id] уникальный номер операции
        :param expert_id: [обязательный если не задан number] идентификатор сотрудника-эксперта
        :param custom_complaint_file: (Передавать путь к файлу) форма "Заявка на возврат", файл, передавать строкой в формате base64. Если файл не передан, то будет удалён.
        :param fields: Расширенный формат вывода. Набор из следующих строк через запятую:
                        "orderPicking" - операция отгрузки, по которой создан возврат
                        "agreement" - договор, по которому выполнена отгрузка
                        "posInfo" - загрузка суммарной информации о позициях
        :return:
        """
        if os.path.isfile(custom_complaint_file):
            with open(custom_complaint_file, "rb") as ccf:
                encoded_string = base64.b64encode(ccf.read()).decode("utf-8")
            custom_complaint_file = f"{encoded_string}"
            del ccf
            del encoded_string
        else:
            raise TypeError('Неверно передан путь к файлу')
        if all(x is None for x in [number, expert_id]):
            raise AbcpParameterRequired('Один из параметров "number" или "expert_id" должен быть указан')
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.update_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.UPDATE, payload, True)

    async def update_custom_file(self, id: Union[int, str], custom_complaint_file: str = '',
                                 fields: Union[List, str] = None):
        """

        :param id: идентификатор операции возврата покупателя
        :param custom_complaint_file: (Передавать путь к файлу) форма "Заявка на возврат", файл, передавать строкой в формате base64. Если файл не передан, то будет удалён.
        :param fields: [необязательный] Расширенный формат вывода
        :return:
        """
        if os.path.isfile(custom_complaint_file):
            with open(custom_complaint_file, "rb") as ccf:
                encoded_string = base64.b64encode(ccf.read()).decode("utf-8")

            custom_complaint_file = f"{encoded_string}"
            del ccf
            del encoded_string
        else:
            raise TypeError('Неверно передан путь к файлу')
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.update_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.UPDATE_CUSTOM_FILE, payload, True)


class DistributorOwners:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def distributor_owners(self, distributor_id: Union[str, int]):
        """
        Получение привязанного контрагента

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D1.80.D0.B8.D0.B2.D1.8F.D0.B7.D0.B0.D0.BD.D0.BD.D0.BE.D0.B3.D0.BE_.D0.BA.D0.BE.D0.BD.D1.82.D1.80.D0.B0.D0.B3.D0.B5.D0.BD.D1.82.D0.B0

        :param distributor_id: Идентификатор поставщика.
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.DistributorOwners.DISTRIBUTOR_OWNERS, payload)


class Orders:
    def __init__(self, base: BaseAbcp):
        self._base = base
        self.messages = Messages(base)

    class _FieldsChecker:
        fields = ["deliveries", "agreement", "tags", "posInfo", "amounts"]

    async def create(self, client_id: Union[str, int], number: Union[int, str] = None,
                     agreement_id: Union[int, str] = None,
                     create_time: Union[datetime, str] = None, manager_id: Union[int, str] = None,
                     fields: Union[List, str] = None):
        """
        Создание заказа

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0

        :param client_id: Идентификатор клиента
        :param number: номер заказа клиента, если не указан, то сформируется согласно шаблону номеров заказов, если указан, то проверяется на уникальность
        :param agreement_id: Идентификатор соглашения (договора)
        :param create_time: дата и время создания заказа, если не указан, заполняется автоматически, не может быть из будущего. `str` в формате RFC3339 или datetime object
        :param manager_id: Идентификатор сотрудника, ответственного за заказ
        :param fields: дополнительная информация ["agreement", "tags", "posInfo", "deliveries", "amounts"]
        :return:
        """
        if isinstance(create_time, datetime):
            create_time = generate(create_time.replace(tzinfo=pytz.utc))
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.CREATE, payload, True)

    async def create_by_cart(self, client_id: Union[str, int], agreement_id: Union[str, int],
                             positions: Union[List, int, str],
                             delivery_address: str, delivery_person: str, delivery_contact: str,
                             number: Union[int, str] = None,
                             create_time: Union[datetime, str] = None, manager_id: Union[int, str] = None,
                             delivery_method_id: Union[int, str] = None,
                             delivery_comment: str = None, delivery_employee_person: str = None,
                             delivery_employee_contact: str = None,
                             delivery_reseller_comment: str = None,
                             delivery_start_time: Union[datetime, str] = None,
                             delivery_end_time: Union[datetime, str] = None,
                             locale: str = None, fields: Union[List, str] = None
                             ):
        """
        Создание заказа по позициям корзины

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0_.D0.BF.D0.BE_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D1.8F.D0.BC_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D1.8B

        :param client_id: Идентификатор клиента
        :param agreement_id: Идентификатор соглашения (договора)
        :param positions: список ID позиций корзины
        :param delivery_address: адрес доставки
        :param delivery_person: контактное лицо
        :param delivery_contact: контакт(телефон) получателя
        :param number: номер заказа клиента, если не указан, то сформируется согласно шаблону номеров заказов, если указан, то проверяется на уникальность
        :param create_time: дата и время создания заказа, если не указан, заполняется автоматически, не может быть из будущего. `str` в формате RFC3339 или datetime object
        :param manager_id: Идентификатор сотрудника, ответственного за заказ
        :param delivery_method_id: 	ID способа доставки
        :param delivery_comment: комментарий
        :param delivery_employee_person: контактный сотрудник
        :param delivery_employee_contact: контакт сотрудника
        :param delivery_reseller_comment: комментарий от магазина
        :param delivery_start_time: время начала интервала доставки
        :param delivery_end_time: время конца интервала доставки
        :param locale: локаль для сохранения описаний товаров ru_RU
        :param fields: дополнительная информация ["agreement", "tags", "posInfo", "deliveries", "amounts"]
        :return:
        """
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        if isinstance(create_time, datetime):
            create_time = generate(create_time.replace(tzinfo=pytz.utc))
        if isinstance(delivery_start_time, datetime):
            delivery_start_time = generate(delivery_start_time.replace(tzinfo=pytz.utc))
        if isinstance(delivery_end_time, datetime):
            delivery_end_time = generate(delivery_end_time.replace(tzinfo=pytz.utc))
        if isinstance(positions, (int, str)):
            positions = [positions]
        payload = generate_payload(
            exclude=['delivery_address', 'delivery_person', 'delivery_contact',
                     'delivery_comment', 'delivery_method_id', 'delivery_employee_person',
                     'delivery_employee_contact', 'delivery_reseller_comment', 'delivery_start_time',
                     'delivery_end_time'],
            **locals())
        return await self._base.request(_Methods.TsAdmin.Orders.CREATE_BY_CART, payload, True)

    async def orders_list(self, number: int = None,
                          agreement_id: Union[int, str] = None,
                          manager_id: Union[int, str] = None,
                          delivery_id: Union[int, str] = None,
                          message: str = None,
                          date_start: Union[datetime, str] = None, date_end: Union[datetime, str] = None,
                          update_date_start: Union[datetime, str] = None, update_date_end: Union[datetime, str] = None,
                          deadline_date_start: Union[datetime, str] = None,
                          deadline_date_end: Union[datetime, str] = None,
                          order_ids: Union[List, int] = None,
                          product_ids: Union[List, int] = None,
                          position_statuses: Union[List, int] = None,
                          skip: int = None,
                          limit: int = None):
        """
        Получение списка заказов

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.BE.D0.B2

        :param number: номер заказа
        :param agreement_id: Идентификатор соглашения
        :param manager_id: Идентификатор менеджера
        :param delivery_id: Идентификатор доставки
        :param message: комментарий к заказу или позиции заказа
        :param date_start: начальная дата диапазона поиска по дате создания заказа(обязательное, если задан dateEnd) `str` в формате RFC3339 или datetime object
        :param date_end: конечная дата диапазона поиска по дате создания заказа(обязательное, если задан dateStart) `str` в формате RFC3339 или datetime object
        :param update_date_start: начальная дата диапазона поиска по дате обновления заказа `str` в формате RFC3339 или datetime object
        :param update_date_end: конечная дата диапазона поиска по дате обновления заказа `str` в формате RFC3339 или datetime object
        :param deadline_date_start: начальная дата диапазона поиска по дате ожидаемой поставки позиций заказа `str` в формате RFC3339 или datetime object
        :param deadline_date_end: конечная дата диапазона поиска по дате ожидаемой поставки позиций заказа `str` в формате RFC3339 или datetime object
        :param order_ids: Идентификаторы заказов через запятую
        :param product_ids: Идентификаторы карточек товаров через запятую
        :param position_statuses: статусы позиций заказов через запятую
        :param skip: количество заказов в ответе, которое нужно пропустить
        :param limit: максимальное количество заказов, которое должно быть возвращено в ответе
        :return:
        """
        if isinstance(position_statuses, list):
            position_statuses = ','.join(map(str, position_statuses))
        if isinstance(product_ids, list):
            product_ids = ','.join(map(str, product_ids))
        if isinstance(order_ids, list):
            order_ids = ','.join(map(str, order_ids))
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(update_date_start, datetime):
            update_date_start = generate(update_date_start.replace(tzinfo=pytz.utc))
        if isinstance(update_date_end, datetime):
            update_date_end = generate(update_date_end.replace(tzinfo=pytz.utc))
        if isinstance(deadline_date_start, datetime):
            deadline_date_start = generate(deadline_date_start.replace(tzinfo=pytz.utc))
        if isinstance(deadline_date_end, datetime):
            deadline_date_end = generate(deadline_date_end.replace(tzinfo=pytz.utc))

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.LIST, payload)

    async def get(self, order_id: Union[str, int]):
        """
        Получение одного заказа

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.B4.D0.BD.D0.BE.D0.B3.D0.BE_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0

        :param order_id: Идентификатор заказа.
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.GET, payload)

    async def refuse(self, order_id: Union[str, int]):
        """
        Отказ от заказа

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9E.D1.82.D0.BA.D0.B0.D0.B7_.D0.BE.D1.82_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0

        :param order_id: Идентификатор заказа.
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.REFUSE, payload, True)

    async def update(self, order_id: Union[str, int], number: Union[str, int] = None, client_id: Union[int, str] = None,
                     agreement_id: Union[int, str] = None,
                     manager_id: Union[int, str] = None, fields: Union[List, str] = None):
        """
        Обновление заказа

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0

        :param order_id: числовой идентификатор заказа
        :param number: 	номер заказа клиента, если не указан, то сформируется согласно шаблону номеров заказов, если указан, то проверяется на уникальность
        :param client_id: Идентификатор клиента
        :param agreement_id: Идентификатор соглашения (договора)
        :param manager_id: Идентификатор сотрудника, ответственного за заказ
        :param fields: дополнительная информация ["agreement", "tags", "posInfo", "deliveries", "amounts"]
        :return:
        """
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.UPDATE, payload, True)

    async def merge(self, main_order_id: Union[str, int], merge_orders_ids: Union[List, str, int] = None,
                    fields: Union[List, str] = None):
        """
        Объединение заказов

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9E.D0.B1.D1.8A.D0.B5.D0.B4.D0.B8.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.BE.D0.B2

        :param main_order_id: Идентификатор главного заказа объединения
        :param merge_orders_ids: массив, идентификаторы остальных заказов объединения
        :param fields: дополнительная информация
        :return:
        """
        if isinstance(merge_orders_ids, (int, str)):
            merge_orders_ids = [merge_orders_ids]
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.MERGE, payload, True)

    async def split(self, order_id: Union[str, int], position_ids: Union[List, str, int] = None,
                    fields: Union[List, str] = None):

        """
        Разделение заказа (В документации описан как второй метод объединения заказов)

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9E.D0.B1.D1.8A.D0.B5.D0.B4.D0.B8.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.BE.D0.B2_2

        :param order_id: Идентификатор заказа разделения
        :param position_ids: массив, идентификаторы отделяемых позиций заказа
        :param fields: дополнительная информация ["agreement", "tags", "posInfo", "deliveries", "amounts"]
        :return:
        """
        if isinstance(position_ids, (int, str)):
            position_ids = [position_ids]
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.SPLIT, payload, True)

    async def reprice(self, order_id: Union[str, int], new_sum: Union[float, int],
                      fields: Union[List, str] = None):
        """
        Изменение суммы заказа

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.83.D0.BC.D0.BC.D1.8B_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0

        :param order_id: Идентификатор заказа клиента
        :param new_sum: новая сумма заказа
        :param fields: дополнительная информация ["agreement", "tags", "posInfo", "deliveries", "amounts"]
        :return:
        """
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.REPRICE, payload, True)


class Messages:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def create(self, order_id: Union[str, int], message: str, employee_id: Union[int, str] = None):
        """
        Создание сообщения

        Source:  https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F

        :param order_id: Идентификатор заказа клиента
        :param message: текст сообщения
        :param employee_id: Идентификатор сотрудника (если не указано, то будет использоваться API-администратор)
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.MESSAGES_CREATE, payload, True)

    async def get_one(self, message_id: Union[str, int]):
        """
        Получение одного сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.B4.D0.BD.D0.BE.D0.B3.D0.BE_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F

        :param message_id: Идентификатор заказа клиента
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.MESSAGES_GET_ONE, payload)

    async def get_list(self, order_id: Union[str, int], skip: int = None, limit: int = None):
        """
        Получение списка сообщений

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D0.B9

        :param order_id: Идентификатор заказа
        :param skip: количество сообщений в ответе, которое нужно пропустить
        :param limit: максимальное количество сообщений в ответе
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.MESSAGES_LIST, payload)

    async def update(self, message_id: Union[str, int], message: str):
        """
        Редактирование сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A0.D0.B5.D0.B4.D0.B0.D0.BA.D1.82.D0.B8.D1.80.D0.BE.D0.B2.D0.B0.D0.BD.D0.B8.D0.B5_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F

        :param message_id: Идентификатор сообщения
        :param message: текст сообщения
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.MESSAGES_UPDATE, payload, True)

    async def delete(self, message_id: Union[str, int]):
        """
        Удаление сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A3.D0.B4.D0.B0.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F

        :param message_id: Идентификатор сообщения
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.MESSAGES_DELETE, payload, True)


class Cart:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def create(self, client_id: Union[str, int], brand: str, number: str, number_fix: Union[str, int],
                     quantity: int,
                     distributor_route_id: Union[str, int], item_key: str, agreement_id: Union[int, str] = None,
                     item_id: Union[int, str] = None):
        """
        Добавление позиции в корзину

        Source:

        :param client_id: идентификатор клиента
        :param brand: бренд
        :param number: артикул по стандарту ABCP
        :param number_fix: Очищенный артикул по стандарту ABCP
        :param quantity: количество товара
        :param distributor_route_id: идентификатор маршрута прайс-листа
        :param item_key: Код товара, полученный поиском search/articles | await api.cp.client.search.articles(602000600, 'Luk')
        :param agreement_id:идентификатор договора, если не указан, то используется активный договор с клиентом по умолчанию
        :param item_id: идентификатор партии на складе
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.CREATE, payload, True)

    async def update(self, position_id: Union[str, int], quantity: int,
                     client_id: Union[int, str] = None, guest_id: Union[int, str] = None,
                     sell_price: Union[str, float, int] = None,
                     cl_to_res_rate: Union[str, float, int] = None, cl_sell_price: Union[str, float, int] = None,
                     availability: int = None, packing: int = None, deadline: int = None, deadline_max: int = None):
        """
        Обновление позиции в корзине

        Source:

        :param position_id: идентификатор позиции в корзине
        :param quantity: новое количество
        :param client_id: идентификатор клиента
        :param guest_id: идентификатор гостя, обязательный, если не задан client_id
        :param sell_price: цена продаже в валюте магазина
        :param cl_to_res_rate: курс между валютой договора с клиентом и валютой магазина
        :param cl_sell_price: цена продаже в валюте договора с клиентом
        :param availability: новое наличие в прайс-листе
        :param packing: новая кратность в прайс-листе
        :param deadline: новый срок поставки
        :param deadline_max: новый максимальный срок поставки
        :return:
        """
        if (client_id is None and guest_id is None) or (client_id is not None and guest_id is not None):
            raise AbcpWrongParameterError(
                'Один и только один из параметров должен быть определён. "client_id", "guest_id"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.UPDATE, payload, True)

    async def get_list(self, client_id: Union[int, str] = None, guest_id: Union[int, str] = None,
                       position_ids: Union[List, str] = None,
                       agreement_id: Union[int, str] = None, skip: int = None, limit: int = None):
        """
        Получение списка позиций в корзине

        Source:

        :param client_id: идентификатор клиента
        :param guest_id: идентификатор гостя
        :param position_ids: список идентификаторов позиций в корзине
        :param agreement_id: идентификатор договора, если не указан, то используется активный договор с клиентом по умолчанию
        :param skip: количество позиций корзины в ответе, которое нужно пропустить
        :param limit: максимальное количество позиций корзины, которое должно быть возвращено в ответе
        :return:
        """
        if isinstance(position_ids, list):
            position_ids = ','.join(map(str, position_ids))
        if (client_id is None and guest_id is None) or (client_id is not None and guest_id is not None):
            raise AbcpWrongParameterError(
                'Один и только один из параметров должен быть определён. "client_id", "guest_id"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.GET_LIST, payload)

    async def exist(self, client_id: Union[str, int], agreement_id: Union[str, int], brand: Union[str, int],
                    number_fix: Union[str, int]):
        """
        Проверка наличия позиции в корзине

        Source:

        :param client_id: идентификатор клиента
        :param agreement_id: идентификатор договора
        :param brand: бренд
        :param number_fix: Очищенный артикул по стандарту ABCP
        :return: quantity - количество найденных позиций в корзине
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.EXIST, payload)

    async def summary(self, client_id: Union[int, str] = None, guest_id: Union[int, str] = None,
                      agreement_id: Union[str, int] = None):
        """
        Получение суммарной информации по позициям корзины

        Source:

        :param client_id: идентификатор клиента
        :param guest_id: идентификатор гостя, обязательный, если не задан client_id
        :param agreement_id: идентификатор договора, если не указан, то используется активный договор с клиентом по умолчанию
        :return:
        """
        if all(x is None for x in [client_id, guest_id]):
            raise AbcpWrongParameterError(
                'Один из параметров должен быть определён. "client_id", "guest_id"')
        if client_id is not None and guest_id is not None:
            raise AbcpWrongParameterError(
                'Один и только один из параметров должен быть определён. "client_id", "guest_id"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.SUMMARY, payload)

    async def clear(self, agreement_id: Union[str, int], client_id: Union[int, str] = None,
                    guest_id: Union[int, str] = None):
        """
        Очистка корзины выбранного договора

        Source:

        :param agreement_id: идентификатор договора
        :param client_id: идентификатор клиента
        :param guest_id: идентификатор гостя, обязательный, если не задан client_id
        :return:
        """
        if all(x is None for x in [client_id, guest_id]):
            raise AbcpWrongParameterError(
                'Один из параметров должен быть определён. "client_id", "guest_id"')
        if client_id is not None and guest_id is not None:
            raise AbcpWrongParameterError(
                'Один и только один из параметров должен быть определён. "client_id", "guest_id"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.CLEAR, payload, True)

    async def delete_positions(self, position_ids: Union[List, str, int],
                               client_id: Union[int, str] = None, guest_id: Union[int, str] = None):
        """
        Удаление позиций корзины

        Source:

        :param position_ids: массив идентификаторов позиций
        :param client_id: идентификатор клиента
        :param guest_id: идентификатор гостя, обязательный, если не задан client_id
        :return:
        """
        if (client_id is None and guest_id is None) or (client_id is not None and guest_id is not None):
            raise AbcpWrongParameterError(
                'Один и только один из параметров должен быть определён. "client_id", "guest_id"')
        if not isinstance(position_ids, list):
            position_ids = [position_ids]

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.DELETE, payload, True)

    async def transfer(self, guest_id: Union[str, int], client_id: Union[str, int]):
        """
        Передача позиций корзины гостя клиенту

        Source:

        :param guest_id: идентификатор гостя
        :param client_id: идентификатор клиента
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.TRANSFER, payload, True)


class Positions:
    def __init__(self, base: BaseAbcp):
        self._base = base
        self.messages = PositionsMessages(base)

    class _FieldsChecker:
        additional_info = ["reserv", "product", "orderPicking",
                           "customerComplaintPoses", "supplierOrder", "grPosition",
                           "order", "delivery", "tags", "unpaidAmount"]
        statuses = ["prepayment", "canceled", "new",
                    "supOrder", "supOrderCanceled", "reservation",
                    "orderPicking", "delivery", "finished"]

    async def get(self, position_id: Union[str, int], additional_info: Union[List, str] = None):
        """
        Получение одной позиции

        Source:

        :param position_id: идентификатор позиции заказа
        :param additional_info: доп. информация позиции ["reserv", "product", "orderPicking",
                           "customerComplaintPoses", "supplierOrder", "grPosition",
                           "order", "delivery", "tags", "unpaidAmount"]
        :return:
        """
        if additional_info is not None:
            additional_info = check_fields(additional_info, self._FieldsChecker.additional_info)

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.GET, payload)

    async def get_list(self, brand: str = None, message: str = None, agreement_id: Union[int, str] = None,
                       client_id: Union[int, str] = None,
                       manager_id: Union[int, str] = None,
                       no_manager_assigned: bool = False,
                       delivery_id: Union[int, str] = None,
                       date_start: str = None, date_end: str = None, update_date_start: str = None,
                       update_date_end: str = None,
                       deadline_date_start: str = None, deadline_date_end: str = None,
                       order_picking_date_start: str = None, order_picking_date_end: str = None,
                       order_picking_good_ids: Union[List, str, int] = None,
                       customer_complaint_position_ids: Union[List, str, int] = None,
                       so_position_ids: Union[List, str, int] = None,
                       route_ids: Union[List, str, int] = None,
                       distributor_ids: Union[List, str, int] = None,
                       ids: Union[List, str, int] = None,
                       order_ids: Union[List, str, int] = None,
                       product_ids: Union[List, str, int] = None,
                       statuses: Union[List, str] = None,
                       tag_ids: Union[List, str, int] = None,
                       limit: int = None, skip: int = None):
        """
        Получение списка позиций

        Source:

        :param brand: бренд товара, полное совпадение
        :param message: комментарий к позиции
        :param agreement_id: идентификатор соглашения
        :param client_id: идентификатор клиента
        :param manager_id: идентификатор менеджера
        :param no_manager_assigned: флаг, добавляющий в выборку позиции без назначенного менеджера; используется с manager_id
        :param delivery_id: идентификатор операции доставки
        :param date_start: минимальная дата создания позиций заказов `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :param date_end: максимальная дата создания позиций заказов `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :param update_date_start: минимальная дата обновления заказов `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :param update_date_end: максимальная дата обновления заказов `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :param deadline_date_start: минимальная дата ожидаемая дата поставки на склад `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :param deadline_date_end: максимальная дата ожидаемая дата поставки на склад `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :param order_picking_date_start: минимальная дата связанной отгрузки `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :param order_picking_date_end: максимальная дата связанной отгрузки `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :param order_picking_good_ids: идентификаторы позиций отгрузки
        :param customer_complaint_position_ids: идентификаторы позиций возврата
        :param so_position_ids: идентификаторы позиций заказов поставщикам
        :param route_ids: идентификаторы маршрутов
        :param distributor_ids: идентификаторы прайс-листов
        :param ids: идентификаторы позиций заказов клиентов
        :param order_ids: идентификаторы заказов клиентов
        :param product_ids: идентификаторы карточек товаров
        :param statuses: список статусов позиций заказов
        :param tag_ids: id тегов
        :param limit: ограничение по кол-ву заказов в выдаче
        :param skip: смещение (по умолчанию 0)
        :return:
        """
        if isinstance(date_start, datetime):
            date_start = f'{date_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(date_end, datetime):
            date_end = f'{date_end:%Y-%m-%d %H:%M:%S}'
        if isinstance(update_date_start, datetime):
            update_date_start = f'{update_date_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(update_date_end, datetime):
            update_date_end = f'{update_date_end:%Y-%m-%d %H:%M:%S}'
        if isinstance(deadline_date_start, datetime):
            deadline_date_start = f'{deadline_date_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(deadline_date_end, datetime):
            deadline_date_end = f'{deadline_date_end:%Y-%m-%d %H:%M:%S}'
        if isinstance(order_picking_date_start, datetime):
            order_picking_date_start = f'{order_picking_date_start:%Y-%m-%d %H:%M:%S}'
        if isinstance(order_picking_date_end, datetime):
            order_picking_date_end = f'{order_picking_date_end:%Y-%m-%d %H:%M:%S}'
        if isinstance(order_picking_good_ids, (int, str)):
            order_picking_good_ids = [order_picking_good_ids]
        if isinstance(customer_complaint_position_ids, (int, str)):
            customer_complaint_position_ids = [customer_complaint_position_ids]
        if isinstance(product_ids, (int, str)):
            product_ids = [product_ids]
        if isinstance(so_position_ids, (int, str)):
            so_position_ids = [so_position_ids]
        if isinstance(route_ids, (int, str)):
            route_ids = [route_ids]
        if isinstance(distributor_ids, (int, str)):
            distributor_ids = [distributor_ids]
        if isinstance(ids, (int, str)):
            ids = [ids]
        if isinstance(order_ids, (int, str)):
            order_ids = [order_ids]
        if isinstance(statuses, str):
            statuses = [statuses]
        if isinstance(tag_ids, list):
            tag_ids = ','.join(map(str, tag_ids))
        if statuses is not None:
            statuses = check_fields(statuses, self._FieldsChecker.statuses)
        if isinstance(no_manager_assigned, bool):
            no_manager_assigned = str(no_manager_assigned)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.GET_LIST, payload)

    async def create(self, order_id: Union[str, int], client_id: Union[str, int], route_id: Union[str, int],
                     distributor_id: Union[str, int], item_key: str,
                     quantity: Union[float, int], sell_price: Union[int, float],
                     brand: Union[str, int], number_fix: str, number: Union[int, str]):
        """
        Создание позиции

        Source:

        :param order_id: идентификатор заказа клиента
        :param client_id: идентификатор клиента
        :param route_id: идентификатор маршрута прайс-листа
        :param distributor_id: идентификатор прайс-листа
        :param item_key: Код товара, полученный поиском search/articles | await api.cp.client.search.articles(602000600, 'Luk')
        :param quantity: количество
        :param sell_price: цена продаже в валюте магазина
        :param brand: бренд
        :param number_fix: номер очищенный
        :param number: номер по формату в ответе от поставщика (из результата поиска)

        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.CREATE, payload, True)

    async def update(self, position_id: Union[str, int], route_id: Union[int, str] = None,
                     distributor_id: Union[int, str] = None,
                     quantity: Union[int, float] = None,
                     sell_price: Union[float, int] = None, cl_to_res_rate: Union[float, int] = None,
                     cl_sell_price: Union[float, int] = None,
                     price_data_sell_price: Union[float, int] = None,
                     prepayment_amount: Union[float, int] = None,
                     deadline_time: Union[datetime, str] = None, deadline_time_max: Union[datetime, str] = None,
                     client_refusal: bool = None,
                     delivery_id: Union[int, str] = None,
                     status: str = None,
                     ):
        """
        Обновление позиции

        Source:

        :param position_id: идентификатор позиции заказа
        :param route_id: идентификатор маршрута прайс-листа
        :param distributor_id: идентификатор прайс-листа
        :param quantity: количество
        :param sell_price: цена продажи в валюте магазина
        :param cl_to_res_rate: курс между валютой договора с клиентом и валютой магазина
        :param cl_sell_price: цена продаже в валюте договора с клиентом
        :param price_data_sell_price: стоимость товара при проценке
        :param prepayment_amount: сумма предоплаты, при 0 будет рассчитана автоматически
        :param deadline_time: срок поставки на склад в формате  `str` в формате RFC3339 или datetime object
        :param deadline_time_max: максимальный поставки на склад в формате  `str` в формате RFC3339 или datetime object
        :param client_refusal: признак желания клиента отказаться от покупки товара
        :param delivery_id: идентификатор операции доставки
        :param status: string, статус позиции, Новый или Предоплата
        :return:
        """
        if isinstance(deadline_time, datetime):
            deadline_time = generate(deadline_time.replace(tzinfo=pytz.utc))
        if isinstance(deadline_time_max, datetime):
            deadline_time_max = generate(deadline_time_max.replace(tzinfo=pytz.utc))
        if isinstance(status, str) and all(status != x for x in ['new', 'prepayment']):
            raise AbcpWrongParameterError('Параметр "status" может принимать значения "new" или "prepayment"')
        if isinstance(client_refusal, bool):
            client_refusal = str(client_refusal)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.UPDATE, payload, True)

    async def cancel(self, position_id: Union[str, int]):
        """
        Аннулирование позиции

        Source:

        :param position_id: идентификатор позиции заказа
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.CANCEL, payload, True)

    async def mass_cancel(self, position_ids: Union[List, int]):
        """
        Массовое аннулирование позиций

        Source:

        :param position_ids: идентификаторы позиций через запятую
        :return:
        """
        if isinstance(position_ids, list):
            position_ids = ','.join(map(str, position_ids))
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MASS_CANCEL, payload, True)

    async def change_status(self, position_ids: Union[List, int], status: str):
        """
        Массовая смена статуса позиций

        Source:

        :param position_ids: идентификатор позиций через запятую
        :param status: принимает значения: new, prepayment
        :return:
        """
        if all(status != x for x in ['new', 'prepayment']):
            raise AbcpWrongParameterError('Параметр "status" может принимать значения "new" или "prepayment"')
        if isinstance(position_ids, list):
            position_ids = ','.join(map(str, position_ids))
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.CHANGE_STATUS, payload, True)

    async def split(self, position_id: Union[str, int], quantity: Union[int, float]):
        """
        Разделение позиции

        Source:

        :param position_id: числовой идентификатор позиции заказа клиента
        :param quantity: количество, которое требуется отделить
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.SPLIT, payload, True)

    async def merge(self, main_position_id: Union[str, int], merge_positions_ids: Union[List, int]):
        """
        Объединение позиций

        Source:

        :param main_position_id:
        :param merge_positions_ids:
        :return:
        """
        if isinstance(merge_positions_ids, list):
            merge_positions_ids = ','.join(map(str, merge_positions_ids))
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MERGE, payload, True)


class PositionsMessages:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get_list(self, position_id: Union[str, int], skip: int = None, limit: int = None):
        """
        Получение списка сообщений

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D0.B9_2

        :param position_id: числовой идентификатор позиции заказа клиента
        :param skip: количество сообщений в ответе, которое нужно пропустить
        :param limit: максимальное количество сообщений, которое должно быть возвращено в ответе
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MESSAGES_LIST, payload)

    async def get(self, message_id: Union[str, int]):
        """
        Получение одного сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.B4.D0.BD.D0.BE.D0.B3.D0.BE_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F_2

        :param message_id: числовой идентификатор сообщения
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MESSAGES_GET, payload)

    async def create(self, position_id: Union[str, int], message: str, employee_id: Union[int, str] = None,
                     date: Union[str, datetime] = None):
        """
        Создание сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F_2

        :param position_id: идентификатор позиции
        :param message: текст сообщения
        :param employee_id: идентификатор сотрудника
        :param date: дата и время. `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :return:
        """
        if isinstance(date, datetime):
            date = f'{date:%Y-%m-%d %H:%M:%S}'
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MESSAGES_CREATE, payload, True)

    async def update(self, message_id: Union[str, int], message: str, employee_id: Union[int, str] = None):
        """
        Редактирование сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A0.D0.B5.D0.B4.D0.B0.D0.BA.D1.82.D0.B8.D1.80.D0.BE.D0.B2.D0.B0.D0.BD.D0.B8.D0.B5_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F_2

        :param message_id: идентификатор сообщения
        :param message: текст сообщения
        :param employee_id: идентификатор сотрудника
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MESSAGES_UPDATE, payload, True)

    async def delete(self, message_id: Union[str, int]):
        """
        Удаление сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A3.D0.B4.D0.B0.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F_2

        :param message_id: идентификатор сообщения
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MESSAGES_DELETE, payload, True)


class GoodReceipts:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def create(self,
                     supplier_id: Union[str, int],
                     positions: Union[List[Dict[str, str]], Dict[str, str]],
                     sup_number: str = None, sup_shipment_date: Union[str, datetime] = None):
        """
        Создаёт приёмку с позициями. Дата создания устанавливается текущая.

        Место хранения указывается в панели управления в разделе Настройки склада -> общие.

        Source:

        :param supplier_id: Идентификатор поставщика
        :param positions: список позиций
        :param sup_number: 	номер отгрузки поставщика
        :param sup_shipment_date: дата и время отгрузки поставщика. `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :return: id `obj`
        """
        if isinstance(sup_shipment_date, datetime):
            sup_shipment_date = f'{sup_shipment_date:%Y-%m-%d %H:%M:%S}'
        if isinstance(positions, dict):
            positions = [positions]
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.CREATE, payload, True)

    async def get(self, limit: int = None, skip: int = None,
                  output: str = None,
                  auto: str = None,
                  creator_id: Union[str, int] = None, worker_id: Union[str, int] = None,
                  agreement_id: str = None, statuses: Union[List, int] = None,
                  number: str = None,
                  date_start: Union[datetime, str] = None, date_end: Union[datetime, str] = None,
                  sup_number: str = None):
        """
        Получение списка операций приёмки

        Source:


        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param skip: количество операций в ответе, которое нужно пропустить
        :param output: формат вывода, флаг 'd' - загрузка удалённых операций, 'e' - загрузка дополнительной информации (договора), 's' - суммы по позициям, кол-во позиций
        :param auto: автоопределяемое поле (поиск по частичному номеру операции или идентификатору, если задано число)
        :param creator_id: идентификатор сотрудника-создателя
        :param worker_id: идентификатор сотрудника-исполнителя
        :param agreement_id: идентификатор договора
        :param statuses: статусы (1 - новая, 2 - в работе, 3 - завершена) List[1, 2, 3] or `int` 2
        :param number: номер операций
        :param date_start: начальная дата диапазона поиска  `str` в формате RFC3339 или datetime object
        :param date_end: конечная  дата диапазона поиска  `str` в формате RFC3339 или datetime object
        :param sup_number: номер отгрузки поставщика
        :return:
        """
        if isinstance(limit, int) and not 1 <= limit <= 1000:
            raise AbcpWrongParameterError('Параметр "limit" должен быть в диапазоне от 1 до 1000')
        if isinstance(output, str) and not all(x in 'des' for x in output):
            raise AbcpWrongParameterError('Параметр "output" должен состоять из  ["d", "e", "s"]')
        if isinstance(statuses, int) and not 1 <= statuses <= 3:
            raise AbcpWrongParameterError('Параметр "statuses" принимет значения от 1 до 3')
        if isinstance(statuses, list):
            if all(1 <= x <= 3 for x in statuses):
                statuses = ','.join(map(str, statuses))
            else:
                raise AbcpWrongParameterError('Параметр "statuses" принимет значения от 1 до 3')
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.GET, payload)

    async def get_positions(self, op_id: Union[str, int], limit: int = None, skip: int = None,
                            output: str = None, product_id: Union[int, str] = None, auto: str = None):
        """
        Получение списка позиций приёмки

        Source:

        :param op_id: идентификатор операции
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param skip: количество операций в ответе, которое нужно пропустить
        :param output: формат вывода, 'e' - загрузка дополнительной информации (справочные товары)
        :param product_id: идентификатор товара справочника
        :param auto: автоопределяемое поле
        :return:
        """

        if isinstance(limit, int) and not 1 <= limit <= 1000:
            raise AbcpWrongParameterError('Параметр "limit" должен быть в диапазоне от 1 до 1000')
        if isinstance(output, str) and output != 'e':
            raise AbcpWrongParameterError('Параметр "output" принимает только значение "e"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.GET_POSITIONS, payload)

    async def update(self, id: int, sup_number: Union[str, int] = None, sup_shipment_date: Union[str, datetime] = None):
        """
        Операция изменения приёмки

        Source:

        :param id: Идентификатор операции приёмки
        :param sup_number: номер отгрузки поставщика
        :param sup_shipment_date: дата и время отгрузки поставщика. `str` в формате %Y-%m-%d %H:%M:%S или datetime object
        :return:
        """

        if isinstance(sup_shipment_date, datetime):
            sup_shipment_date = f'{sup_shipment_date:%Y-%m-%d %H:%M:%S}'
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.UPDATE, payload, True)

    async def change_status(self, id: int, status: int):
        """
        Операция изменения статуса приёмки

        Source:

        :param id: Идентификатор операции приёмки
        :param status: id нового статуса приёмки
        :return:
        """
        if not 1 <= status <= 3:
            raise AbcpWrongParameterError('Параметр "status" принимает значения от 1 до 3')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.CHANGE_STATUS, payload, True)

    async def delete(self, id: int):
        """
        Операция удаления приёмки

        Source:

        :param id: Идентификатор операции приёмки
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.DELETE, payload, True)

    async def create_position(self, op_id: Union[str, int], loc_id: Union[str, int], product_id: Union[str, int],
                              brand: Union[str, int], number: Union[int, str],
                              quantity: Union[float, int], sup_buy_price: Union[float, int],
                              manufacturer_country: str = None, gtd: str = None, warranty_period: int = None,
                              return_period: int = None, barcodes: Union[List, List, str, int] = None,
                              comment: str = None,
                              descr: str = None, expected_quantity: Union[float, int] = None,
                              so_position_id: str = None,
                              old_order_position_id: Union[int, str] = None):
        """
        Операция создания позиции приёмки

        Source:

        :param op_id: идентификатор приёмки
        :param loc_id: идентификатор места хранения
        :param product_id: идентификатор товара в справочнике
        :param brand: Название производителя.
        :param number: Номер детали (код производителя)
        :param quantity: Количество
        :param sup_buy_price: Цена позиции в валюте поставщика
        :param manufacturer_country: Страна производитель - три английские буквы: RUS - Россия, CNH - Китай, DEU - Германия и т.д.
        :param gtd: Номер ГТД
        :param warranty_period: Срок гарантийного обслуживания с момента продажи в днях
        :param return_period: Срок гарантированного возврата в днях
        :param barcodes: Штрихкод или Штрихкоды в List
        :param comment: Комментарий
        :param descr: Описание будущей партии
        :param expected_quantity: Ожидаемое кол-во товара
        :param so_position_id: Идентификатор позиции заказа поставщику, на основании которой была создана позиция приемки
        :param old_order_position_id: Идентификатор позиции старого заказа, на основании которой была создана позиция приемки
        :return:
        """
        if isinstance(barcodes, list):
            barcodes = ' '.join(barcodes)
        if isinstance(manufacturer_country, str) and len(manufacturer_country) != 3:
            raise AbcpWrongParameterError('Параметр manufacturer_country должен состоять из 3 английских букв')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.CREATE_POSITION, payload, True)

    async def delete_position(self, id: int):
        """
        Операция удаления позиции приёмки

        Source:

        :param id: Идентификатор позиции приёмки
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.DELETE_POSITION, payload, True)

    async def get_position(self, id: int):
        """
        Операция получения позиции приёмки

        Source:

        :param id: Идентификатор позиции приёмки
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.GET_POSITION, payload)

    async def update_position(self, id: int, brand: str, number: str,
                              quantity: Union[float, int], sup_buy_price: Union[float, int],
                              manufacturer_country: str = None, gtd: str = None, warranty_period: int = None,
                              return_period: int = None, barcodes: Union[List, List, str, int] = None,
                              comment: str = None,
                              descr: str = None, expected_quantity: Union[float, int] = None,
                              so_position_id: str = None,
                              old_order_position_id: Union[int, str] = None):
        """
        Операция изменения позиции приёмки

        Source:

        :param id: Идентификатор позиции приёмки
        :param brand: Название производителя.
        :param number: Номер детали (код производителя)
        :param quantity: Номер детали (код производителя)
        :param sup_buy_price: Цена позиции в валюте поставщика
        :param manufacturer_country: Страна производитель - три английские буквы: RUS - Россия, CNH - Китай, DEU - Германия и т.д.
        :param gtd: Номер ГТД
        :param warranty_period: Срок гарантийного обслуживания с момента продажи в днях
        :param return_period: Срок гарантированного возврата в днях
        :param barcodes: Штрихкод или Штрихкоды в List
        :param comment: Комментарий
        :param descr: Описание будущей партии
        :param expected_quantity: Ожидаемое кол-во товара
        :param so_position_id: Идентификатор позиции заказа поставщику, на основании которой была создана позиция приемки
        :param old_order_position_id: Идентификатор позиции старого заказа, на основании которой была создана позиция приемки
        :return: dict
        """
        if isinstance(barcodes, list):
            barcodes = ' '.join(map(str, barcodes))
        if isinstance(manufacturer_country, str) and len(manufacturer_country) != 3:
            raise AbcpWrongParameterError('Параметр manufacturer_country должен состоять из 3 английских букв')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.UPDATE_POSITION, payload, True)


class Tags:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def list(self, ids: Union[str, List[str], List[int]] = None):
        """
        Операция получения списка тегов

        :param ids: Идентификаторы тегов через запятую
        :return: dict
        """
        if isinstance(ids, list):
            ids = ','.join(map(str, ids))
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Tags.LIST, payload)

    async def create(self, name: str, color: str):
        """
        Операция создания тега

        :param name: Имя тега
        :param color: Цвет тега
        :return:
        """
        if not color.startswith('#'):
            try:
                check_hex = int(color, base=16)
                del check_hex
                color = f'#{color}'
            except ValueError as exc:
                raise AbcpWrongParameterError(
                    'The "color" must be a hexadecimal string. It is possible to specify both with and without "#"') from exc

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Tags.CREATE, payload, True)

    async def delete(self, id: Union[str, int]):
        """
        Операция удаления тега


        :param id: Идентификатор удаляемого тега
        :return:
        """
        if isinstance(id, str) and not id.isdigit():
            raise AbcpWrongParameterError('Параметр "id" должен быть числом')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Tags.DELETE, payload, True)


class TagsRelationships:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def list(self, object_ids: Union[str, List[str], List[int]] = None,
                   object_type: Union[str, int] = None,
                   group_by_object_id: Union[bool, int] = None,
                   with_all_tags: Union[bool, int] = None,
                   tags_ids: Union[str, List[str], List[int]] = None):

        """

        :param object_ids: Необязателен. Идентификаторы объектов через запятую
        :param object_type: Необязателен. Тип объекта
        :param group_by_object_id: Необязателен. Группировать теги по id объекта
        :param with_all_tags: Необязателен. оставит только объекты, на которых есть все теги из tagIds
        :param tags_ids: Необязателен. Идентификаторы тегов через запятую
        :return:
        """
        if isinstance(object_ids, list):
            object_ids = ','.join(map(str, object_ids))

        if isinstance(object_type, str) and object_type.isdigit():
            if not 1 <= int(object_type) <= 13:
                raise AbcpWrongParameterError('"object_type" must be in range 1-13')
        if isinstance(object_type, int) and not 1 <= object_type <= 13:
            raise AbcpWrongParameterError('"object_type" must be in range 1-13')
        if isinstance(group_by_object_id, bool):
            group_by_object_id = int(group_by_object_id)
        if isinstance(group_by_object_id, int) and not 0 <= group_by_object_id <= 1:
            raise AbcpWrongParameterError('"group_by_object_id" must be in range 0-1 or use a Boolean value')

        if isinstance(with_all_tags, bool):
            with_all_tags = int(with_all_tags)
        if isinstance(with_all_tags, int) and not 0 <= with_all_tags <= 1:
            raise AbcpWrongParameterError('"with_all_tags" must be in range 0-1 or use a Boolean value')
        if with_all_tags is not None and tags_ids is None:
            raise AbcpParameterRequired('The "with_all_tags" parameter must be used with the "tags_ids" parameter')

        if isinstance(tags_ids, list):
            tags_ids = ','.join(map(str, tags_ids))
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.TagsRelationships.LIST, payload)

    async def create(self, tag_id: Union[str, int], object_id: Union[str, int], object_type: Union[str, int]):
        """
        Операция создания связи тега

        :param tag_id: 	Идентификатор тега
        :param object_id: Идентификатор объекта
        :param object_type: Тип объекта
        :return:
        """
        if isinstance(tag_id, str) and not tag_id.isdigit():
            raise AbcpWrongParameterError('Параметр "tag_id" должен быть числом')

        if isinstance(object_id, str) and not object_id.isdigit():
            raise AbcpWrongParameterError('Параметр "object_id" должен быть числом')

        if isinstance(object_type, str) and object_type.isdigit():
            if not 1 <= int(object_type) <= 13:
                raise AbcpWrongParameterError('"object_type" must be in range 1-13')
        if isinstance(object_type, int) and not 1 <= object_type <= 13:
            raise AbcpWrongParameterError('"object_type" must be in range 1-13')

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.TagsRelationships.CREATE, payload, True)

    async def delete(self, tag_id: Union[str, int], object_id: Union[str, int], object_type: Union[str, int]):
        """
        Операция удаления связи тега

        :param tag_id: 	Идентификатор тега
        :param object_id: Идентификатор объекта
        :param object_type: Тип объекта
        :return:
        """

        if isinstance(tag_id, str) and not tag_id.isdigit():
            raise AbcpWrongParameterError('Параметр "tag_id" должен быть числом')

        if isinstance(object_id, str) and not object_id.isdigit():
            raise AbcpWrongParameterError('Параметр "object_id" должен быть числом')

        if isinstance(object_type, str) and object_type.isdigit():
            object_type = int(object_type)
        if isinstance(object_type, int) and not 1 <= object_type <= 13:
            raise AbcpWrongParameterError('"object_type" must be in range 1-13')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.TagsRelationships.DELETE, payload, True)


class Payments:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @dataclass(frozen=True)
    class _Status:
        status = ["new", "inProcess", "accepted", "rejected", "canceled"]

    async def get_list(self,
                       contractor_id: Union[str, int] = None, agreement_id: Union[str, int] = None,
                       amount_start: Union[float, int, str] = None, amount_end: Union[float, int, str] = None,
                       status: Union[List[str], str] = None,
                       number: str = None,
                       requisite_id: Union[str, int] = None,
                       skip: int = None, limit: int = None,
                       payment_type: Union[List[str], str] = None, payment_method_ids: Union[List[int], int] = None,
                       date_start: Union[datetime, str] = None, date_end: Union[datetime, str] = None,
                       fields: Union[List[str], str] = None):
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(status, list):
            if any(x not in self._Status.status for x in status):
                raise AbcpWrongParameterError(
                    f'Неверный список статусов: {status} Допустимые статусы {self._Status.status}')
            status = ','.join(status)
        if isinstance(payment_method_ids, list):
            payment_method_ids = ','.join(map(str, payment_method_ids))
        if isinstance(payment_type, list):
            payment_type = ','.join(payment_type)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Payments.GET_LIST, payload)

    async def create(self,
                     payment_type: str, payment_method_id: int,
                     agreement_id: int, author_id: int,
                     amount: Union[float, int, str], date: Union[datetime, str],
                     contractor_id: int = None, commission: Union[float, int] = None,
                     comment: str = None, fields: Union[List[str], str] = None):
        if isinstance(date, datetime):
            date = generate(date.replace(tzinfo=pytz.utc))
        if isinstance(fields, list):
            fields = ','.join(fields)

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Payments.CREATE, payload)


class PaymentMethods:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @dataclass(frozen=True)
    class _Fields:
        allow_change_param = ["yes", "no", "paymentInterfaceOnly", "editOnly"]

    async def get_list(self,
                       payment_type: Optional[str] = None,
                       allow_change_payment: Optional[str] = None,
                       state: Optional[str] = None):
        """
        Получение списка способов оплаты

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D0.BF.D0.BE.D1.81.D0.BE.D0.B1.D0.BE.D0.B2_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82.D1.8B

        :param payment_type: Тип оплаты
        :param allow_change_payment: Вариант доступности изменения платежа
        :param state: Состояние
        :return:
        """
        if isinstance(allow_change_payment, str) and allow_change_payment not in self._Fields.allow_change_param:
            raise AbcpWrongParameterError(f'Неверное значение параметра "allow_change_payment" {allow_change_payment}.'
                                          f'Допустимые значения {self._Fields.allow_change_param}')

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.PaymentMethods.METHODS_LIST, payload)


class Agreements:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get_list(self, contractor_ids: Union[int, str, List[int]] = None,
                       contractor_requisite_ids: Union[int, str, List[int]] = None,
                       shop_requisite_ids: Union[int, str, List[int]] = None,
                       is_active: bool = None, is_delete: bool = None, is_default: bool = None,
                       agreement_type: int = None, relation_type: int = None,
                       number: str = None, currency: str = None,
                       date_start: Union[datetime, str] = None, date_end: Union[datetime, str] = None,
                       credit_limit: Union[float, int] = None,
                       limit: int = None, skip: int = None):
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))

        if isinstance(contractor_ids, int) or isinstance(contractor_ids, str):
            contractor_ids = [contractor_ids]
        if isinstance(contractor_requisite_ids, int) or isinstance(contractor_requisite_ids, str):
            contractor_requisite_ids = [contractor_requisite_ids]
        if isinstance(shop_requisite_ids, int) or isinstance(shop_requisite_ids, str):
            shop_requisite_ids = [shop_requisite_ids]
        if isinstance(is_active, bool):
            is_active = str(is_active)
        if isinstance(is_delete, bool):
            is_delete = str(is_delete)
        if isinstance(is_default, bool):
            is_default = str(is_default)


        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Agreements.get_list, payload)


class LegalPersons:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get_list(self, ids: Union[str, List[str]] = None, contractor_id: Optional[int] = None,
                       form: Optional[int] = None, org_type: Optional[int] = None,
                       agreement_with_individuals_required: Optional[int] = None,
                       with_tax_systems: Optional[int] = None,
                       limit: Optional[int] = None, offset: Optional[int] = None):
        if isinstance(ids, list):
            ids = ','.join(map(str, ids))
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.LegalPersons.get_list, payload)
