import base64
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any

from ..api import _Methods
from ..base import BaseAbcp
from ..exceptions import AbcpWrongParameterError, AbcpParameterRequired
from ..utils.fields_checker import check_fields, check_limit, process_ts_lists, process_ts_dates, ensure_list_params, \
    process_cp_dates, convert_bool_params_to_str
from ..utils.payload import generate_payload


class SupplierReturnsOperations:
    def __init__(self, base: BaseAbcp):
        self._base = base

    class _FieldsChecker:
        list_fields = ["goodsReceipt", "agreement", "tags", ]

    @check_limit
    @process_ts_lists('agreement_ids', 'tag_ids', 'sbis_statuses')
    @process_ts_dates('date_start', 'date_end')
    async def get_list(self, creator_id: str | int = None, supplier_id: str | int = None,
                       goods_receipt_id: str | int = None,
                       agreement_ids: List[int] | int | str = None,
                       tag_ids: List[int] | int | str = None,
                       sbis_statuses: List[str] | str = None,
                       date_start: str | datetime = None,
                       date_end: str | datetime = None,
                       skip: int = None, limit: int = None, fields: List | str = None
                       ):
        """
        Получение списка операций возврата поставщику

        :param creator_id: идентификатор сотрудника-создателя
        :param supplier_id: идентификатор поставщика
        :param goods_receipt_id: идентификатор приходной операции
        :param agreement_ids: список идентификаторов договоров
        :param tag_ids: список идентификаторов тегов
        :param sbis_statuses: список статусов в системе СБИС
        :param date_start: начальная дата диапазона поиска
        :param date_end: конечная дата диапазона поиска
        :param skip: количество операций, которое нужно пропустить
        :param limit: максимальное количество операций в ответе
        :param fields: дополнительные поля для вывода
        :return: список операций возврата поставщику
        """
        payload = generate_payload(**locals())

        if fields is not None:
            payload["fields"] = check_fields(fields, self._FieldsChecker.list_fields)

        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.LIST, payload)

    @check_limit
    @process_ts_lists('agreement_ids', 'tag_ids', 'sbis_statuses')
    @process_ts_dates('date_start', 'date_end')
    async def get_sum(self, creator_id: str | int = None, supplier_id: str | int = None,
                      goods_receipt_id: str | int = None,
                      agreement_ids: List[int] | int | str = None,
                      tag_ids: List[int] | int | str = None,
                      sbis_statuses: List[str] | str = None,
                      date_start: str | datetime = None,
                      date_end: str | datetime = None,
                      skip: int = None, limit: int = None
                      ):
        """
        Получение суммы операций возврата поставщику

        :param creator_id: идентификатор сотрудника-создателя
        :param supplier_id: идентификатор поставщика
        :param goods_receipt_id: идентификатор приходной операции
        :param agreement_ids: список идентификаторов договоров
        :param tag_ids: список идентификаторов тегов
        :param sbis_statuses: список статусов в системе СБИС
        :param date_start: начальная дата диапазона поиска
        :param date_end: конечная дата диапазона поиска
        :param skip: количество операций, которое нужно пропустить
        :param limit: максимальное количество операций в ответе
        :return: сумма операций возврата поставщику
        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.SUM, payload)

    async def get(self, id: str | int):
        """
        Получение операции возврата поставщику

        :param id: идентификатор операции
        :return: операция возврата поставщику
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.GET, payload)

    async def create(self, creator_id: str | int, supplier_id: str | int,
                     goods_receipt_id: str | int, agreement_id: str | int):
        """
        Создание операции возврата поставщику

        :param creator_id: идентификатор сотрудника-создателя
        :param supplier_id: идентификатор поставщика
        :param goods_receipt_id: идентификатор приходной операции
        :param agreement_id: идентификатор договора
        :return: результат операции создания
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.CREATE, payload, post=True)

    async def update(self, id: str | int, number: str = None, fields: List | str = None):
        """
        Обновление операции возврата поставщику

        :param id: идентификатор операции
        :param number: номер операции
        :param fields: дополнительные поля для вывода
        :return: результат операции обновления
        """
        payload = generate_payload(**locals())

        if fields is not None:
            payload["fields"] = check_fields(fields, self._FieldsChecker.list_fields)

        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.UPDATE, payload, post=True)

    async def delete(self, id: str | int):
        """
        Удаление операции возврата поставщику

        :param id: идентификатор операции
        :return: результат операции удаления
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Operations.DELETE, payload, post=True)


class SupplierReturnsPositions:
    def __init__(self, base: BaseAbcp):
        self._base = base

    class _FieldsChecker:
        list_fields = ["item", "location", "operationInfo", "tags",
                       "goodsReceiptPos", "availableQuantity", "customerComplaintPos"]

    @check_limit
    @process_ts_lists('goods_receipt_pos_ids', 'item_ids', 'goods_receipt_ids')
    @process_ts_dates('date_start', 'date_end')
    async def get_list(self, op_id: str | int = None, status: int = None, type: int = None,
                       goods_receipt_pos_ids: List[str] | str = None,
                       item_ids: List[str] | str = None,
                       supplier_id: str = None,
                       goods_receipt_ids: List[str] | str = None,
                       date_start: str | datetime = None,
                       date_end: str | datetime = None,
                       skip: int = None,
                       limit: int = None,
                       fields: List[str] | str = None):
        """
        Получение списка позиций возврата поставщику

        :param op_id: идентификатор операции
        :param status: статус позиции
        :param type: тип позиции
        :param goods_receipt_pos_ids: список идентификаторов позиций прихода
        :param item_ids: список идентификаторов партий
        :param supplier_id: идентификатор поставщика
        :param goods_receipt_ids: список идентификаторов операций прихода
        :param date_start: начальная дата диапазона поиска
        :param date_end: конечная дата диапазона поиска
        :param skip: количество позиций, которое нужно пропустить
        :param limit: максимальное количество позиций в ответе
        :param fields: дополнительные поля для вывода
        :return: список позиций возврата поставщику
        """
        payload = generate_payload(**locals())

        if fields is not None:
            payload["fields"] = check_fields(fields, self._FieldsChecker.list_fields)

        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.LIST, payload)

    @check_limit
    @process_ts_lists('goods_receipt_pos_ids', 'item_ids', 'goods_receipt_ids')
    @process_ts_dates('date_start', 'date_end')
    async def get_sum(self, op_id: str | int = None, status: int = None, type: int = None,
                      goods_receipt_pos_ids: List[str] | str = None,
                      item_ids: List[str] | str = None,
                      supplier_id: str = None,
                      goods_receipt_ids: List[str] | str = None,
                      date_start: str | datetime = None,
                      date_end: str | datetime = None,
                      skip: int = None,
                      limit: int = None,
                      fields: List[str] | str = None):
        """
        Получение суммы позиций возврата поставщику

        :param op_id: идентификатор операции
        :param status: статус позиции
        :param type: тип позиции
        :param goods_receipt_pos_ids: список идентификаторов позиций прихода
        :param item_ids: список идентификаторов партий
        :param supplier_id: идентификатор поставщика
        :param goods_receipt_ids: список идентификаторов операций прихода
        :param date_start: начальная дата диапазона поиска
        :param date_end: конечная дата диапазона поиска
        :param skip: количество позиций, которое нужно пропустить
        :param limit: максимальное количество позиций в ответе
        :param fields: дополнительные поля для вывода
        :return: сумма позиций возврата поставщику
        """
        payload = generate_payload(**locals())

        if fields is not None:
            payload["fields"] = check_fields(fields, self._FieldsChecker.list_fields)

        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.SUM, payload)

    async def status(self):
        """
        Получение возможных статусов позиций возврата поставщику

        :return: список статусов
        """
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.STATUS)

    async def get(self, id: str | int):
        """
        Получение позиции возврата поставщику

        :param id: идентификатор позиции
        :return: позиция возврата поставщику
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.GET, payload)

    @ensure_list_params('poses_data')
    async def create_multiple(self, op_id: str | int, poses_data: List[Dict] | Dict):
        """
        Создание позиций возврата поставщику

        :param op_id: идентификатор операции
        :param poses_data: список данных позиций или одна позиция
        :return: результат операции создания
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.CREATE_MULTIPLE, payload, post=True)

    async def split(self, id: str | int, quantity: int | float,
                    fields: List[str] | str = None):
        """
        Разделение позиции возврата поставщику

        :param id: идентификатор позиции
        :param quantity: количество для разделения
        :param fields: дополнительные поля для вывода
        :return: результат операции разделения
        """
        payload = generate_payload(**locals())

        if fields is not None:
            payload["fields"] = check_fields(fields, self._FieldsChecker.list_fields)

        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.SPLIT, payload, post=True)

    async def update(self, id: str | int, type: int = None, loc_id: str | int = None,
                     quantity: int | float = None, comment: str = None,
                     fields: List[str] | str = None):
        """
        Обновление позиции возврата поставщику

        :param id: идентификатор позиции
        :param type: тип позиции
        :param loc_id: идентификатор места хранения
        :param quantity: количество
        :param comment: комментарий
        :param fields: дополнительные поля для вывода
        :return: результат операции обновления
        """
        payload = generate_payload(**locals())

        if fields is not None:
            payload["fields"] = check_fields(fields, self._FieldsChecker.list_fields)

        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.UPDATE, payload, post=True)

    async def change_status(self, id: str | int, status: int, fields: List[str] | str = None):
        """
        Изменение статуса позиции возврата поставщику

        :param id: идентификатор позиции
        :param status: новый статус
        :param fields: дополнительные поля для вывода
        :return: результат операции изменения статуса
        """
        payload = generate_payload(**locals())

        if fields is not None:
            payload["fields"] = check_fields(fields, self._FieldsChecker.list_fields)

        return await self._base.request(_Methods.TsAdmin.SupplierReturns.Positions.CHANGE_STATUS, payload, post=True)


class SupplierReturnsPositionsAttr:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def create(self, id: str | int, attr: Dict):
        """
        Создание атрибута позиции возврата поставщику

        :param id: идентификатор позиции
        :param attr: данные атрибута
        :return: результат операции создания
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.PositionsAttr.CREATE, payload, post=True)

    async def update(self, id: str | int, old_name: str, new_name: str, description: str):
        """
        Обновление атрибута позиции возврата поставщику

        :param id: идентификатор позиции
        :param old_name: текущее имя атрибута
        :param new_name: новое имя атрибута
        :param description: описание атрибута
        :return: результат операции обновления
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.PositionsAttr.UPDATE, payload, post=True)

    async def delete(self, id: str | int, name: str):
        """
        Удаление атрибута позиции возврата поставщику

        :param id: идентификатор позиции
        :param name: имя атрибута
        :return: результат операции удаления
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.SupplierReturns.PositionsAttr.DELETE, payload, post=True)


class SupplierReturns:
    def __init__(self, base: BaseAbcp):
        self._base = base
        self._operations: SupplierReturnsOperations | None = None
        self._positions: SupplierReturnsPositions | None = None
        self._positions_attr: SupplierReturnsPositionsAttr | None = None

    @property
    def operations(self) -> SupplierReturnsOperations:
        """
        Получить доступ к операциям возврата поставщику

        :return: Объект для работы с операциями возврата поставщику
        :rtype: SupplierReturnsOperations
        """
        if self._operations is None:
            self._operations = SupplierReturnsOperations(self._base)
        return self._operations

    @property
    def positions(self) -> SupplierReturnsPositions:
        """
        Получить доступ к позициям возврата поставщику

        :return: Объект для работы с позициями возврата поставщику
        :rtype: SupplierReturnsPositions
        """
        if self._positions is None:
            self._positions = SupplierReturnsPositions(self._base)
        return self._positions

    @property
    def positions_attr(self) -> SupplierReturnsPositionsAttr:
        """
        Получить доступ к атрибутам позиций возврата поставщику

        :return: Объект для работы с атрибутами позиций возврата поставщику
        :rtype: SupplierReturnsPositionsAttr
        """
        if self._positions_attr is None:
            self._positions_attr = SupplierReturnsPositionsAttr(self._base)
        return self._positions_attr


class OrderPickings:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @process_ts_dates('date', 'execution_date')
    @ensure_list_params('positions')
    async def fast_get_out(self, client_id: str | int, supplier_id: str | int,
                           positions: List[Dict] | Dict, distributor_id: str | int = None,
                           route_id: str | int = None, location_id: str | int = None,
                           order_picking_reseller_data: Dict = None,
                           number: str | int = None, date: str | datetime = None,
                           execution_date: str | datetime = None
                           ):
        """
        Операция быстрого создания заказа, приёмки, расхода

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9E.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D1.8F_.D0.B1.D1.8B
        .D1.81.D1.82.D1.80.D0.BE.D0.B3.D0.BE_.D1.81.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D1.8F_.D0.B7.D0.B0.D0.BA.D0
        .B0.D0.B7.D0.B0.2C_.D0.BF.D1.80.D0.B8.D1.91.D0.BC.D0.BA.D0.B8.2C_.D1.80.D0.B0.D1.81.D1.85.D0.BE.D0.B4.D0.B0


        :param client_id: Идентификатор клиента. :param supplier_id: Идентификатор поставщика. :param positions:
        Массив объектов позиций отгрузки. :obj:`dict` или :obj:`List[Dict]` :param distributor_id: Идентификатор
        прайс-листа. :param route_id: Идентификатор маршрута. :param location_id: Идентификатор места хранения.
        :param order_picking_reseller_data: Дополнительная информация в формате json, которая будет сохранена в
        операцию отгрузки :param number: Номер отгрузки, если пустой, то будет заполнен автоматически :param date:
        Дата отгрузки, если пустая, то будет заполнена автоматически. `str` в формате RFC3339 или datetime object
        :param execution_date: [необязательный] Дата проведения/выполнения в формате RFC3339, если пустая,
        то будет заполнена из `date` :return: None
        """
        payload = generate_payload(exclude=['positions'], **locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.FAST_GET_OUT, payload, post=True)

    @check_limit
    @process_ts_dates('date_start', 'date_end')
    @process_ts_lists('statuses', 'co_old_pos_ids')
    async def get(self, id: str | int = None, client_id: str | int = None, limit: int = None,
                  skip: int = None,
                  output: str = None, auto: str = None, creator_id: str | int = None,
                  worker_id: str | int = None,
                  agreement_id: str | int = None, statuses: List | str | int = None,
                  number: int = None, date_start: str | datetime = None, date_end: str | datetime = None,
                  co_old_pos_ids: List | str | int = None):

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.GET, payload, post=True)

    @check_limit
    async def get_goods(self, op_id: str | int, limit: int = None, skip: int = None,
                        output: str = None, product_id: str | int = None, item_id: str | int = None,
                        ignore_canceled: int | bool = None):

        if isinstance(op_id, str) and not op_id.isdigit():
            raise AbcpWrongParameterError("op_id", op_id, "должен быть числом или строкой, содержащей число")

        if isinstance(ignore_canceled, int):
            if ignore_canceled == 0:
                ignore_canceled = None
            elif ignore_canceled != 1:
                raise AbcpWrongParameterError(
                    "ignore_canceled", ignore_canceled, "должен быть 1 (True) или 0 (False)")
        if isinstance(ignore_canceled, bool):
            if ignore_canceled:
                ignore_canceled = int(ignore_canceled)
            else:
                ignore_canceled = None
        if isinstance(output, str) and any(x not in ["e", "o"] for x in output):
            raise AbcpWrongParameterError("output", output, 'должен содержать только флаги "e", "o"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.GET_GOODS, payload)

    @process_ts_dates('create_date')
    @process_ts_lists('pp_ids')
    async def create_by_old_pos(self, agreement_id: str | int, account_details_id: str | int,
                                loc_id: str | int,
                                pp_ids: List | str | int,
                                create_date: str | datetime = None, op_id: str | int = None,
                                status_id: str | int = None,
                                done_right_away: int | bool = None, output: str = None):
        """
        Создаёт новую операцию отгрузки на основе созданных позиций старого заказа. Source:
        https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.BE.D0.BF.D0.B5.D1
        .80.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D1.82.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B8_.D0.BD.D0.B0_.D0.BE.D1.81.D0.BD
        .D0.BE.D0.B2.D0.B5_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B9_.D1.81.D1.82.D0.B0.D1.80.D0.BE.D0.B3.D0.BE_.D0
        .B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0

        :param agreement_id: Идентификатор договора клиента
        :param account_details_id: Идентификатор реквизитов магазина
        :param loc_id: Идентификатор места хранения [необязательный], если не указано,
         то используется основное место хранения
        :param pp_ids: список идентификаторов позиций старого заказа
        :param create_date: дата создания, если не указана, то используется Текущая
        :param op_id: идентификатор созданной операции [обязательный] - Если op_id заполнен,
        то система будет работать в режиме обновления существующей операции
        (передача позиций без автосоздания операции, с добавлением к существующей)
        :param status_id: идентификатор статуса новым позициям операции [необязательный], если не указан,
        то используется id с номером 1
        :param done_right_away: флаг автоматического завершения операции 1 или 0 [необязательный параметр].
        При значении 1 позиции операции будут автоматически завершены, если это возможно.
        :param output: формат вывода, флаг 'e' - загрузка дополнительной информации
            (договора, места хранения, доставки, упаковки), 't' - загрузка информации о тегах, 's' - суммы по позициям,
             кол-во позиций, 'r' - загрузка пользовательских дополнительных данных ("reseller_data")
        :return: Created OrderPicking id
        """
        if isinstance(done_right_away, bool):
            done_right_away = int(done_right_away)

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.CREATE_BY_OLD_POS, payload, post=True)

    async def change_status(self, id: int, operation_status_id: str | int,
                            positions_status_id: str | int = None):
        """
        Меняет статус операции отгрузки и, при необходимости, дочерних позиций этой операции.

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81
        .D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BE.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D1.82.D0.B3.D1
        .80.D1.83.D0.B7.D0.BA.D0.B8_.D0.B8.2C_.D0.BF.D1.80.D0.B8_.D0.BD.D0.B5.D0.BE.D0.B1.D1.85.D0.BE.D0.B4.D0.B8.D0
        .BC.D0.BE.D1.81.D1.82.D0.B8.2C_.D0.B4.D0.BE.D1.87.D0.B5.D1.80.D0.BD.D0.B8.D1.85_.D0.BF.D0.BE.D0.B7.D0.B8.D1
        .86.D0.B8.D0.B9_.D1.8D.D1.82.D0.BE.D0.B9_.D0.BE.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D0.B8

        :param id: Идентификатор операции отгрузки, которой нужно изменить статус
        :param operation_status_id: Идентификатор нового статуса операции
        :param positions_status_id: Идентификатор нового статуса для всех позиций операции.
        :return: OrderPicking
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.CHANGE_STATUS, payload, post=True)

    async def update(self, id: int, number: str | int = None, creator_id: str | int = None,
                     worker_id: str | int = None,
                     client_id: str | int = None,
                     agreement_id: str | int = None, account_details_id: str | int = None,
                     loc_id: str | int = None,
                     reseller_data: Dict = None):
        """
        Обновление общей информации об операции отгрузка.

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_
        .D0.BE.D0.B1.D1.89.D0.B5.D0.B9_.D0.B8.D0.BD.D1.84.D0.BE.D1.80.D0.BC.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D0.B1_.D0
        .BE.D0.BF.D0.B5.D1.80.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D1.82.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B0

        :param id: Идентификатор операции отгрузки
        :param number: Номер операции отгрузки
        :param creator_id: Идентификатор сотрудника-создателя
        :param worker_id: Идентификатор сотрудника-исполнителя
        :param client_id: Идентификатор клиента
        :param agreement_id: Идентификатор договора клиента
        :param account_details_id: Идентификатор реквизитов магазина
        :param loc_id: Идентификатор места хранения [необязательный], если не указано,
         то используется основное место хранения
        :param reseller_data: Дополнительная информация в формате json, которая будет сохранена в операцию отгрузки
        :return: OrderPicking
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.OrderPickings.UPDATE, payload, post=True)

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

    @check_limit
    @process_ts_dates('date_start', 'date_end')
    @process_ts_lists('position_statuses')
    async def get(self, id: int = None, client_id: str | int = None, creator_id: str | int = None,
                  expert_id: str | int = None,
                  auto: str | int = None,
                  number: int = None, order_picking_id: str | int = None,
                  position_statuses: List | int = None,
                  position_type: int = None, position_auto: str | int = None,
                  date_start: str | datetime = None,
                  date_end: str | datetime = None,
                  skip: int = None, limit: int = None, fields: List | str = None):
        """
        Получение списка возвратов покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81
        .D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.BE.D0.B2_.D0.BF.D0.BE.D0.BA.D1
        .83.D0.BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

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
        if isinstance(position_type, int) and (position_type < 1 or position_type > 3):
            raise AbcpWrongParameterError("position_type", position_type, "должен быть в диапазоне от 1 до 3")
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.get_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.GET, payload)

    @process_ts_dates('date_start', 'date_end')
    @process_ts_lists('tag_ids', 'picking_ids', 'old_co_position_ids', 'order_picking_good_ids')
    async def get_positions(self, op_id: str | int = None, order_picking_good_id: str | int = None,
                            order_picking_good_ids: List | int = None,
                            picking_ids: List | int = None,
                            old_co_position_ids: List | int = None,
                            client_id: str | int = None, old_item_id: str | int = None,
                            item_id: str | int = None,
                            tag_ids: List | int = None,
                            loc_id: str | int = None, status: int = None, type: int = None,
                            date_start: str | datetime = None,
                            date_end: str | datetime = None,
                            skip: int = None, limit: int = None,
                            sort: str = None, output: str = None,
                            fields: List | str = None):
        """
        Получение списка позиций операции возврата покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81
        .D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B9_.D0.BE.D0.BF.D0.B5.D1.80.D0.B0.D1
        .86.D0.B8.D0.B8_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.82
        .D0.B5.D0.BB.D1.8F

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
            raise AbcpWrongParameterError("sort", sort, 'может принимать значения "status" или "createDate"')

        if isinstance(status, int) and not 1 <= status <= 8:
            raise AbcpWrongParameterError("status", status, "должен быть в диапазоне от 1 до 8")
        if isinstance(type, int) and not 1 <= type <= 3:
            raise AbcpWrongParameterError("type", type, "должен быть в диапазоне от 1 до 3")
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.get_positions_fields)
        payload = generate_payload(exclude=['old_item_id'], **locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.GET_POSITIONS, payload)

    @ensure_list_params('positions')
    async def create(self, order_picking_id: str | int, positions: List[Dict] | Dict):
        """
        Создание возврата покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.B2.D0.BE
        .D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param order_picking_id: Идентификатор операции отгрузки из которой возвращается товар
        :param positions: Список позиций.
        :return:
        """
        payload = generate_payload(exclude=['positions'], **locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.CREATE, payload, post=True)

    async def create_position(self, op_id: str | int, order_picking_position_id: str | int, quantity: int,
                              type: int, comment: str):
        """
        Создание позиции возврата покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE
        .D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BE.D0.BA.D1.83.D0
        .BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param op_id: Идентификатор операции возврата
        :param order_picking_position_id: Идентификатор позиции отгрузки
        :param quantity: количество к возврату
        :param type: тип возврата(1-возврат, 2-отказ, 3-брак)
        :param comment:комментарий
        :return:
        """
        if not 1 <= type <= 3:
            raise AbcpWrongParameterError("type", type, "должен быть в диапазоне от 1 до 3")
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.CREATE_POSITION, payload,
                                        post=True)

    @ensure_list_params('positions')
    async def create_position_multiple(self, positions: List[Dict] | Dict,
                                       customer_complaint_id: int,
                                       customer_complaint: str,
                                       custom_complaint_file: str = None):
        with open(custom_complaint_file, "rb") as ccf:
            encoded_string = base64.b64encode(ccf.read()).decode("utf-8")
        custom_complaint_file = f"{encoded_string}"
        del ccf
        del encoded_string
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.CREATE_POSITION_MULTIPLE, payload,
                                        post=True)

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
            raise AbcpParameterRequired('Необходим хотя бы один из параметров: quantity, type, comment')
        if isinstance(type, int) and not 1 <= type <= 3:
            raise AbcpWrongParameterError("type", type, "должен быть в диапазоне от 1 до 3")
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.UPDATE_POSITION, payload,
                                        post=True)

    async def change_position_status(self, id: int, status: int):
        """
        Изменение статуса позиции возврата покупателя

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.98.D0.B7.D0.BC.D0.B5.D0.BD.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B2.D0.BE.D0.B7.D0.B2.D1.80.D0.B0.D1.82.D0.B0_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.82.D0.B5.D0.BB.D1.8F

        :param id:
        :param status:
        :return:
        """
        if not (1 <= status <= 8):
            raise AbcpWrongParameterError("status", status, "должен быть в диапазоне от 1 до 8")
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.CHANGE_STATUS_POSITION, payload,
                                        post=True)

    async def update(self, id: str | int, number: int = None, expert_id: str | int = None,
                     custom_complaint_file: str = '',
                     fields: List | str = None):
        """

        :param id: [обязательный] идентификатор операции возврата покупателя
        :param number: [обязательный если не задан expert_id] уникальный номер операции
        :param expert_id: [обязательный если не задан number] идентификатор сотрудника-эксперта
        :param custom_complaint_file: (Передавать путь к файлу) форма "Заявка на возврат", файл, передавать строкой в формате base64. Если файл не передан, то будет удалён.
        :param fields: Расширенный формат вывода. Набор из следующих строк через запятую:
                        "orderPicking" - операция отгрузки, по которой создан возврат
        :return:
        """
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.update_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.UPDATE, payload, post=True)

    async def update_custom_file(self, id: str | int, custom_complaint_file: str = '',
                                 fields: List | str = None):
        """
        Обновление файла акта о браке.
        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D1.84.D0.B0.D0.B9.D0.BB.D0.B0_.D0.B0.D0.BA.D1.82.D0.B0_.D0.BE_.D0.B1.D1.80.D0.B0.D0.BA.D0.B5

        :param id: [обязательный] идентификатор операции возврата покупателя
        :param custom_complaint_file: (Передавать путь к файлу) форма "Заявка на возврат", файл, передавать строкой в формате base64. Если файл не передан, то будет удалён.
        :param fields: Расширенный формат вывода. Набор из следующих строк через запятую:
                        "orderPicking" - операция отгрузки, по которой создан возврат
        :return:
        """
        try:
            with open(custom_complaint_file, "rb") as ccf:
                encoded_string = base64.b64encode(ccf.read()).decode("utf-8")
            custom_complaint_file = f"{encoded_string}"
            del ccf
            del encoded_string
        except FileNotFoundError:
            pass
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.update_fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.CustomerComplaints.UPDATE_CUSTOM_FILE, payload,
                                        post=True)


class DistributorOwners:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def distributor_owners(self, distributor_id: str | int):
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

    @process_ts_dates('create_time')
    async def create(self, client_id: str | int, number: str | int = None,
                     agreement_id: str | int = None,
                     create_time: str | datetime = None, manager_id: str | int = None,
                     fields: List | str = None):
        """
        Создание заказа

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0

        :param client_id: Идентификатор клиента
        :param number: Номер заказа
        :param agreement_id: Идентификатор договора
        :param create_time: Время создания. `str` в формате RFC3339 или datetime object
        :param manager_id: Идентификатор менеджера
        :param fields: расширенный формат вывода
        :return:
        """

        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.CREATE, payload, post=True)

    @process_ts_dates('create_time', 'delivery_start_time', 'delivery_end_time')
    @process_ts_lists('positions')
    async def create_by_cart(self, client_id: str | int, agreement_id: str | int,
                             positions: List | int | str,
                             delivery_address: str, delivery_person: str, delivery_contact: str,
                             number: str | int = None,
                             create_time: str | datetime = None, manager_id: str | int = None,
                             delivery_method_id: str | int = None,
                             delivery_comment: str = None, delivery_employee_person: str = None,
                             delivery_employee_contact: str = None,
                             delivery_reseller_comment: str = None,
                             delivery_start_time: str | datetime = None,
                             delivery_end_time: str | datetime = None,
                             locale: str = None, fields: List | str = None
                             ):
        """
        Создание заказа из корзины

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A1.D0.BE.D0.B7.D0.B4.D0.B0.D0.BD.D0.B8.D0.B5_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.B0_.D0.B8.D0.B7_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D1.8B

        :param client_id: Идентификатор клиента
        :param agreement_id: Идентификатор договора
        :param positions: Список идентификаторов позиций корзины, которые следует оформить в заказ. Если не указан, берутся все позиции корзины, принадлежащие текущему соглашению.
        :param delivery_address: Адрес доставки
        :param delivery_person: ФИО контактного лица
        :param delivery_contact: Телефон контактного лица
        :param number: Номер заказа. Если не указан, будет создан автоматически.
        :param create_time: Дата и время создания заказа. Если не указаны, будут взяты текущие дата и время. `str` в формате RFC3339 или datetime object
        :param manager_id: Идентификатор менеджера
        :param delivery_method_id: Идентификатор способа доставки
        :param delivery_comment: Комментарий к доставке
        :param delivery_employee_person: ФИО сотрудника доставки
        :param delivery_employee_contact: Телефон сотрудника доставки
        :param delivery_reseller_comment: Дополнительный комментарий
        :param delivery_start_time: Дата и время начала периода доставки. `str` в формате RFC3339 или datetime object
        :param delivery_end_time: Дата и время конца периода доставки. `str` в формате RFC3339 или datetime object
        :param locale: Локаль. Задается в формате language[_territory], например, ru_RU. По умолчанию используется локаль сайта.
        :param fields: расширенный формат вывода
        :return:
        """

        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.CREATE_BY_CART, payload, post=True)

    @check_limit
    @process_ts_lists('order_ids', 'product_ids', 'position_statuses')
    @process_ts_dates('date_start', 'date_end',
                      'update_date_start', 'update_date_end',
                      'deadline_date_start', 'deadline_date_end')
    async def orders_list(self, number: int = None,
                          agreement_id: str | int = None,
                          manager_id: str | int = None,
                          delivery_id: str | int = None,
                          message: str = None,
                          date_start: str | datetime = None, date_end: str | datetime = None,
                          update_date_start: str | datetime = None, update_date_end: str | datetime = None,
                          deadline_date_start: str | datetime = None,
                          deadline_date_end: str | datetime = None,
                          order_ids: List | int = None,
                          product_ids: List | int = None,
                          position_statuses: List | int = None,
                          skip: int = None,
                          limit: int = None):
        """
        Получение списка заказов клиентов

        :param number: Номер заказа
        :param agreement_id: Идентификатор договора для фильтрации. Если не указан, будут возвращены заказы по всем договорам
        :param manager_id: Идентификатор менеджера. Если не указан и менеджер не присвоен, будут возвращены заказы без менеджера
        :param delivery_id: Идентификатор способа доставки для фильтрации. Если не указан, будут возвращены заказы по всем способам доставки
        :param message: Текстовый поиск по номеру заказа или комментарию
        :param date_start: Минимальная дата создания заказа. `str` в формате RFC3339 или datetime object
        :param date_end: Максимальная дата создания заказа. `str` в формате RFC3339 или datetime object
        :param update_date_start: Минимальная дата изменения заказа. `str` в формате RFC3339 или datetime object
        :param update_date_end: Максимальная дата изменения заказа. `str` в формате RFC3339 или datetime object
        :param deadline_date_start: Минимальная дата поставки. `str` в формате RFC3339 или datetime object
        :param deadline_date_end: Максимальная дата поставки заказа. `str` в формате RFC3339 или datetime object
        :param order_ids: Идентификаторы заказов для фильтрации
        :param product_ids: Идентификаторы товаров для фильтрации
        :param position_statuses: Статусы заказа для фильтрации
        :param skip: Количество пропускаемых записей
        :param limit: Количество получаемых записей
        :return: List[Order]
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.LIST, payload)

    async def get(self, order_id: str | int):
        """
        Получение конкретного заказа по ID
        :param order_id: Идентификатор заказа
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.GET, payload)

    async def refuse(self, order_id: str | int):
        """
        Отказ от заказа
        Меняет статус заказа на "Отказ". Товар при этом не списывается со склада.
        :param order_id: Идентификатор заказа
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.REFUSE, payload, post=True)

    async def update(self, order_id: str | int, number: str | int = None, client_id: str | int = None,
                     agreement_id: str | int = None,
                     manager_id: str | int = None, fields: List | str = None):
        """
        Изменение заказа клиента
        :param order_id: Идентификатор заказа
        :param number: Номер заказа
        :param client_id: Идентификатор клиента
        :param agreement_id: Идентификатор договора
        :param manager_id: Идентификатор менеджера
        :param fields: расширенный формат вывода
        :return:
        """
        if all(x is None for x in [number, client_id, agreement_id, manager_id]):
            raise AbcpParameterRequired(
                'Необходим хотя бы один из параметров: number, client_id, agreement_id, manager_id')
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.UPDATE, payload, post=True)

    @process_ts_lists('merge_orders_ids')
    async def merge(self, main_order_id: str | int, merge_orders_ids: List | str | int = None,
                    fields: List | str = None):
        """
        Объединение нескольких заказов в один
        :param main_order_id: Идентификатор основного заказа
        :param merge_orders_ids: Идентификаторы заказов, которые объединяются с main_order_id
        :param fields: расширенный формат вывода
        :return:
        """
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.MERGE, payload, post=True)

    @process_ts_lists('position_ids')
    async def split(self, order_id: str | int, position_ids: List | str | int = None,
                    fields: List | str = None):
        """
        Разделение заказа
        :param order_id: Идентификатор заказа
        :param position_ids: Идентификаторы позиций заказа
        :param fields: расширенный формат вывода
        :return:
        """
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.SPLIT, payload, post=True)

    async def reprice(self, order_id: str | int, new_sum: int | float,
                      fields: List | str = None):
        """
        Изменение цены заказа
        :param order_id: Идентификатор заказа
        :param new_sum: Новая сумма заказа
        :param fields: расширенный формат вывода
        :return:
        """
        if fields is not None:
            fields = check_fields(fields, self._FieldsChecker.fields)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.REPRICE, payload, post=True)


class Messages:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def create(self, order_id: str | int, message: str, employee_id: str | int = None):
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

    async def get_one(self, message_id: str | int):
        """
        Получение одного сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.B4.D0.BD.D0.BE.D0.B3.D0.BE_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F

        :param message_id: Идентификатор заказа клиента
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.MESSAGES_GET_ONE, payload)

    @check_limit
    async def get_list(self, order_id: str | int, skip: int = None, limit: int = None):
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

    async def update(self, message_id: str | int, message: str):
        """
        Редактирование сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.A0.D0.B5.D0.B4.D0.B0.D0.BA.D1.82.D0.B8.D1.80.D0.BE.D0.B2.D0.B0.D0.BD.D0.B8.D0.B5_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F

        :param message_id: Идентификатор сообщения
        :param message: текст сообщения
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Orders.MESSAGES_UPDATE, payload, True)

    async def delete(self, message_id: str | int):
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

    async def create(self, client_id: str | int, brand: str, number: str, number_fix: str | int,
                     quantity: int,
                     distributor_route_id: str | int, item_key: str, agreement_id: str | int = None,
                     item_id: str | int = None) -> Dict[str, Any]:
        """
        Добавление позиции в корзину клиента администратором

        Добавляет товар в корзину указанного клиента с заданными параметрами.

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.94.D0.BE.D0.B1.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8_.D0.B2_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D1.83

        :param client_id: Идентификатор клиента
        :type client_id: :obj:`str` или :obj:`int`
        :param brand: Бренд товара
        :type brand: :obj:`str`
        :param number: Артикул по стандарту ABCP
        :type number: :obj:`str`
        :param number_fix: Очищенный артикул по стандарту ABCP
        :type number_fix: :obj:`str` или :obj:`int`
        :param quantity: Количество товара
        :type quantity: :obj:`int`
        :param distributor_route_id: Идентификатор маршрута прайс-листа
        :type distributor_route_id: :obj:`str` или :obj:`int`
        :param item_key: Код товара, полученный через поиск search/articles
        :type item_key: :obj:`str`
        :param agreement_id: Идентификатор договора, если не указан, то используется активный договор с клиентом по умолчанию
        :type agreement_id: :obj:`str` или :obj:`int`
        :param item_id: Идентификатор партии на складе
        :type item_id: :obj:`str` или :obj:`int`
        :return: Результат операции добавления в корзину
        :rtype: Dict[str, Any]
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.CREATE, payload, True)

    async def update(self, position_id: str | int, quantity: int,
                     client_id: str | int = None, guest_id: str | int = None,
                     sell_price: str | int | float = None,
                     cl_to_res_rate: str | int | float = None, cl_sell_price: str | int | float = None,
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
            raise AbcpParameterRequired(
                'Должен быть указан один и только один из параметров: "client_id" или "guest_id"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.UPDATE, payload, True)

    @check_limit
    async def get_list(self, client_id: str | int = None, guest_id: str | int = None,
                       position_ids: List | str = None,
                       agreement_id: str | int = None, skip: int = None, limit: int = None):
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
            raise AbcpParameterRequired(
                'Должен быть указан один и только один из параметров: "client_id" или "guest_id"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.GET_LIST, payload)

    async def exist(self, client_id: str | int, agreement_id: str | int, brand: str | int,
                    number_fix: str | int):
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

    async def summary(self, client_id: str | int = None, guest_id: str | int = None,
                      agreement_id: str | int = None):
        """
        Получение суммарной информации по позициям корзины

        Source:

        :param client_id: идентификатор клиента
        :param guest_id: идентификатор гостя, обязательный, если не задан client_id
        :param agreement_id: идентификатор договора, если не указан, то используется активный договор с клиентом по умолчанию
        :return:
        """
        if all(x is None for x in [client_id, guest_id]):
            raise AbcpParameterRequired(
                'Должен быть указан хотя бы один из параметров: "client_id" или "guest_id"')
        if client_id is not None and guest_id is not None:
            raise AbcpParameterRequired(
                'Должен быть указан один и только один из параметров: "client_id" или "guest_id"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.SUMMARY, payload)

    async def clear(self, agreement_id: str | int, client_id: str | int = None,
                    guest_id: str | int = None):
        """
        Очистка корзины выбранного договора

        Source:

        :param agreement_id: идентификатор договора
        :param client_id: идентификатор клиента
        :param guest_id: идентификатор гостя, обязательный, если не задан client_id
        :return:
        """
        if all(x is None for x in [client_id, guest_id]):
            raise AbcpParameterRequired(
                'Должен быть указан хотя бы один из параметров: "client_id" или "guest_id"')
        if client_id is not None and guest_id is not None:
            raise AbcpParameterRequired(
                'Должен быть указан один и только один из параметров: "client_id" или "guest_id"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.CLEAR, payload, True)

    @ensure_list_params('position_ids')
    async def delete_positions(self, position_ids: List | str | int,
                               client_id: str | int = None, guest_id: str | int = None):
        """
        Удаление позиций корзины

        Source:

        :param position_ids: массив идентификаторов позиций
        :param client_id: идентификатор клиента
        :param guest_id: идентификатор гостя, обязательный, если не задан client_id
        :return:
        """
        if (client_id is None and guest_id is None) or (client_id is not None and guest_id is not None):
            raise AbcpParameterRequired(
                'Должен быть указан один и только один из параметров: "client_id" или "guest_id"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Cart.DELETE, payload, True)

    async def transfer(self, guest_id: str | int, client_id: str | int):
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

    async def get(self, position_id: str | int, additional_info: List | str = None):
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

    @check_limit
    @ensure_list_params('order_picking_good_ids', 'customer_complaint_position_ids',
                        'product_ids', 'so_position_ids', 'route_ids',
                        'distributor_ids', 'ids', 'order_ids', 'statuses')
    @process_ts_lists('order_picking_good_ids', 'tag_ids')
    @process_cp_dates('date_start', 'date_end',
                      'update_date_start', 'update_date_end',
                      'deadline_date_start', 'deadline_date_end',
                      'order_picking_date_start', 'order_picking_date_end')
    @convert_bool_params_to_str('no_manager_assigned')
    async def get_list(self, brand: str = None, message: str = None, agreement_id: str | int = None,
                       client_id: str | int = None,
                       manager_id: str | int = None,
                       no_manager_assigned: bool = False,
                       delivery_id: str | int = None,
                       date_start: str = None, date_end: str = None, update_date_start: str = None,
                       update_date_end: str = None,
                       deadline_date_start: str = None, deadline_date_end: str = None,
                       order_picking_date_start: str = None, order_picking_date_end: str = None,
                       order_picking_good_ids: List | str | int = None,
                       customer_complaint_position_ids: List | str | int = None,
                       so_position_ids: List | str | int = None,
                       route_ids: List | str | int = None,
                       distributor_ids: List | str | int = None,
                       ids: List | str | int = None,
                       order_ids: List | str | int = None,
                       product_ids: List | str | int = None,
                       statuses: List | str = None,
                       tag_ids: List | str | int = None,
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
        if statuses is not None:
            statuses = check_fields(statuses, self._FieldsChecker.statuses)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.GET_LIST, payload)

    async def create(self, order_id: str | int, client_id: str | int, route_id: str | int,
                     distributor_id: str | int, item_key: str,
                     quantity: int | float, sell_price: int | float,
                     brand: str | int, number_fix: str, number: str | int):
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

    @process_ts_dates('deadline_time', 'deadline_time_max')
    @convert_bool_params_to_str('client_refusal')
    async def update(self, position_id: str | int, route_id: str | int = None,
                     distributor_id: str | int = None,
                     quantity: int | float = None,
                     sell_price: int | float = None, cl_to_res_rate: int | float = None,
                     cl_sell_price: int | float = None,
                     price_data_sell_price: int | float = None,
                     prepayment_amount: int | float = None,
                     deadline_time: str | datetime = None, deadline_time_max: str | datetime = None,
                     client_refusal: bool = None,
                     delivery_id: str | int = None,
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

        if isinstance(status, str) and all(status != x for x in ['new', 'prepayment']):
            raise AbcpWrongParameterError("status", status, 'может принимать значения "new" или "prepayment"')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.UPDATE, payload, True)

    async def cancel(self, position_id: str | int):
        """
        Аннулирование позиции

        Source:

        :param position_id: идентификатор позиции заказа
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.CANCEL, payload, True)

    @process_ts_lists('position_ids')
    async def mass_cancel(self, position_ids: List | int):
        """
        Массовое аннулирование позиций

        Source:

        :param position_ids: идентификаторы позиций через запятую
        :return:
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MASS_CANCEL, payload, True)

    @process_ts_lists('position_ids')
    async def change_status(self, position_ids: List | int, status: str):
        """
        Массовая смена статуса позиций

        Source:

        :param position_ids: идентификатор позиций через запятую
        :param status: принимает значения: new, prepayment
        :return:
        """
        if all(status != x for x in ['new', 'prepayment']):
            raise AbcpWrongParameterError("status", status, 'может принимать значения "new" или "prepayment"')

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.CHANGE_STATUS, payload, True)

    async def split(self, position_id: str | int, quantity: int | float):
        """
        Разделение позиции

        Source:

        :param position_id: числовой идентификатор позиции заказа клиента
        :param quantity: количество, которое требуется отделить
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.SPLIT, payload, True)

    @process_ts_lists('merge_positions_ids')
    async def merge(self, main_position_id: str | int, merge_positions_ids: List | int):
        """
        Объединение позиций

        Source:

        :param main_position_id:
        :param merge_positions_ids:
        :return:
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MERGE, payload, True)


class PositionsMessages:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @check_limit
    async def get_list(self, position_id: str | int, skip: int = None, limit: int = None):
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

    async def get(self, message_id: str | int):
        """
        Получение одного сообщения

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.B4.D0.BD.D0.BE.D0.B3.D0.BE_.D1.81.D0.BE.D0.BE.D0.B1.D1.89.D0.B5.D0.BD.D0.B8.D1.8F_2

        :param message_id: числовой идентификатор сообщения
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Positions.MESSAGES_GET, payload)

    async def create(self, position_id: str | int, message: str, employee_id: str | int = None,
                     date: str | datetime = None):
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

    async def update(self, message_id: str | int, message: str, employee_id: str | int = None):
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

    async def delete(self, message_id: str | int):
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

    class _FieldsChecker:
        list_fields = ["agreement", "supplier", "creator"]

    @check_limit
    @process_ts_dates('date_start', 'date_end')
    async def get_positions(self, creator_id: str | int = None, supplier_id: str | int = None,
                            agreement_id: str | int = None, status: int = None,
                            date_start: str | datetime = None, date_end: str | datetime = None,
                            skip: int = None, limit: int = None, fields: List | str = None):
        """
        Получение списка приходных операций

        :param creator_id: идентификатор сотрудника-создателя
        :param supplier_id: идентификатор поставщика
        :param agreement_id: идентификатор договора
        :param status: статус операции
        :param date_start: начальная дата диапазона поиска
        :param date_end: конечная дата диапазона поиска
        :param skip: количество операций, которое нужно пропустить
        :param limit: максимальное количество операций в ответе
        :param fields: дополнительные поля для вывода
        :return: список приходных операций
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.GET_POSITIONS, payload)

    async def update(self, id: int, sup_number: str | int = None, sup_shipment_date: str | datetime = None):
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
            raise AbcpWrongParameterError("status", status, "должен быть в диапазоне от 1 до 3")
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

    async def create_position(self, op_id: str | int, loc_id: str | int, product_id: str | int,
                              brand: str | int, number: str | int,
                              quantity: int | float, sup_buy_price: int | float,
                              manufacturer_country: str = None, gtd: str = None, warranty_period: int = None,
                              return_period: int = None, barcodes: List | str | int = None,
                              comment: str = None,
                              descr: str = None, expected_quantity: int | float = None,
                              so_position_id: str = None,
                              old_order_position_id: str | int = None):
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
            raise AbcpWrongParameterError("manufacturer_country", manufacturer_country,
                                          "должен состоять из 3 английских букв")
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
                              quantity: int | float, sup_buy_price: int | float,
                              manufacturer_country: str = None, gtd: str = None, warranty_period: int = None,
                              return_period: int = None, barcodes: List | str | int = None,
                              comment: str = None,
                              descr: str = None, expected_quantity: int | float = None,
                              so_position_id: str = None,
                              old_order_position_id: str | int = None):
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
            raise AbcpWrongParameterError("manufacturer_country", manufacturer_country,
                                          "должен состоять из 3 английских букв")
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.GoodReceipts.UPDATE_POSITION, payload, True)


class Tags:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @process_ts_lists('ids')
    async def list(self, ids: List | str = None):
        """
        Операция получения списка тегов

        :param ids: Идентификаторы тегов через запятую
        :return: dict
        """

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
                    "color",
                    color,
                    "It is possible to specify both with and without \"#\""
                )

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Tags.CREATE, payload, True)

    async def delete(self, id: str | int):
        """
        Операция удаления тега


        :param id: Идентификатор удаляемого тега
        :return:
        """
        if isinstance(id, str) and not id.isdigit():
            raise AbcpWrongParameterError("id", id, "должен быть числом или строкой, содержащей число")
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Tags.DELETE, payload, True)


class TagsRelationships:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @process_ts_lists('object_ids', 'tags_ids')
    async def list(self, object_ids: List | str = None,
                   object_type: str | int = None,
                   group_by_object_id: int | bool = None,
                   with_all_tags: int | bool = None,
                   tags_ids: List | str = None):

        """

        :param object_ids: Необязателен. Идентификаторы объектов через запятую
        :param object_type: Необязателен. Тип объекта
        :param group_by_object_id: Необязателен. Группировать теги по id объекта
        :param with_all_tags: Необязателен. оставит только объекты, на которых есть все теги из tagIds
        :param tags_ids: Необязателен. Идентификаторы тегов через запятую
        :return:
        """

        if (isinstance(object_type, str) and object_type.isdigit()) or isinstance(object_type, int):
            if not 1 <= int(object_type) <= 13:
                raise AbcpWrongParameterError("object_type",
                                              object_type,
                                              "must be in range 1-13"
                                              )
        if isinstance(group_by_object_id, bool):
            group_by_object_id = int(group_by_object_id)
        if isinstance(group_by_object_id, int) and not 0 <= group_by_object_id <= 1:
            raise AbcpWrongParameterError("group_by_object_id", group_by_object_id,
                                          "must be in range 0-1 or use a Boolean value")

        if isinstance(with_all_tags, bool):
            with_all_tags = int(with_all_tags)
        if isinstance(with_all_tags, int) and not 0 <= with_all_tags <= 1:
            raise AbcpWrongParameterError("with_all_tags", with_all_tags, "must be in range 0-1 or use a Boolean value")
        if with_all_tags is not None and tags_ids is None:
            raise AbcpParameterRequired('The "with_all_tags" parameter must be used with the "tags_ids" parameter')

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.TagsRelationships.LIST, payload)

    async def create(self, tag_id: str | int, object_id: str | int, object_type: str | int):
        """
        Операция создания связи тега

        :param tag_id: 	Идентификатор тега
        :param object_id: Идентификатор объекта
        :param object_type: Тип объекта
        :return:
        """
        if isinstance(tag_id, str) and not tag_id.isdigit():
            raise AbcpWrongParameterError("tag_id", tag_id, "должен быть числом или строкой, содержащей число")

        if isinstance(object_id, str) and not object_id.isdigit():
            raise AbcpWrongParameterError("object_id", object_id, "должен быть числом или строкой, содержащей число")

        if (isinstance(object_type, str) and object_type.isdigit()) or isinstance(object_type, int):
            if not 1 <= int(object_type) <= 13:
                raise AbcpWrongParameterError("object_type",
                                              object_type,
                                              "must be in range 1-13"
                                              )

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.TagsRelationships.CREATE, payload, True)

    async def delete(self, tag_id: str | int, object_id: str | int, object_type: str | int):
        """
        Операция удаления связи тега

        :param tag_id: 	Идентификатор тега
        :param object_id: Идентификатор объекта
        :param object_type: Тип объекта
        :return:
        """

        if isinstance(tag_id, str) and not tag_id.isdigit():
            raise AbcpWrongParameterError("tag_id", tag_id, "должен быть числом или строкой, содержащей число")

        if isinstance(object_id, str) and not object_id.isdigit():
            raise AbcpWrongParameterError("object_id", object_id, "должен быть числом или строкой, содержащей число")

        if isinstance(object_type, str) and object_type.isdigit():
            object_type = int(object_type)
        if isinstance(object_type, int) and not 1 <= object_type <= 13:
            raise AbcpWrongParameterError("object_type",
                                          object_type,
                                          "must be in range 1-13"
                                          )
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.TagsRelationships.DELETE, payload, True)


class Payments:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @dataclass(frozen=True)
    class _Status:
        status = ["new", "inProcess", "accepted", "rejected", "canceled"]

    @check_limit
    @process_ts_dates('date_start', 'date_end')
    @process_ts_lists('payment_method_ids', 'tag_ids')
    async def get_list(self,
                       contractor_id: str | int = None, agreement_id: str | int = None,
                       amount_start: str | int | float = None, amount_end: str | int | float = None,
                       status: List[str] | str = None,
                       number: str = None,
                       requisite_id: str | int = None,
                       skip: int = None, limit: int = None,
                       payment_type: List[str] | str = None, payment_method_ids: List | int = None,
                       date_start: str | datetime = None, date_end: str | datetime = None,
                       fields: List[str] | str = None):
        """

        :param contractor_id:
        :param agreement_id:
        :param amount_start:
        :param amount_end:
        :param status:
        :param number:
        :param requisite_id:
        :param skip:
        :param limit:
        :param payment_type:
        :param payment_method_ids:
        :param date_start:
        :param date_end:
        :param fields:
        :return:
        """
        if isinstance(status, list):
            if any(x not in self._Status.status for x in status):
                raise AbcpWrongParameterError(
                    "status",
                    status,
                    f'Допустимые статусы {self._Status.status}')
            status = ','.join(status)
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Payments.GET_LIST, payload)

    @process_ts_dates('date')
    @process_ts_lists('fields')
    async def create(self,
                     payment_type: str, payment_method_id: int,
                     agreement_id: int, author_id: int,
                     amount: str | int | float, date: str | datetime,
                     contractor_id: int = None, commission: int | float = None,
                     comment: str = None, fields: List[str] | str = None):
        """

        :param payment_type:
        :param payment_method_id:
        :param agreement_id:
        :param author_id:
        :param amount:
        :param date:
        :param contractor_id:
        :param commission:
        :param comment:
        :param fields:
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Payments.CREATE, payload)

    @process_ts_dates('date')
    @process_ts_lists('fields')
    async def update(self,
                     payment_id: int | float,
                     agreement_id: int = None,
                     amount: int | float = None,
                     date: str | datetime = None,
                     status: str = None,
                     payment_order: str = None,
                     commission: int | float = None,
                     comment: str = None,
                     fields: List[str] | str = None):
        """
        Обновление платежа

        :param payment_id: Идентификатор платежа
        :param agreement_id: Идентификатор договора
        :param amount: Сумма платежа
        :param date: Дата платежа
        :param status: Статус платежа
        :param payment_order: Номер платежного поручения
        :param commission: Комиссия
        :param comment: Комментарий
        :param fields: Дополнительные поля для вывода
        :return: Результат операции обновления
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Payments.UPDATE, payload, post=True)


class PaymentMethods:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @dataclass(frozen=True)
    class _Fields:
        allow_change_param = ["yes", "no", "paymentInterfaceOnly", "editOnly"]

    async def get_list(self,
                       payment_type: str | None = None,
                       allow_change_payment: str | None = None,
                       state: str | None = None):
        """
        Получение списка способов оплаты

        Source: https://www.abcp.ru/wiki/API.TS.Admin#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D0.BF.D0.BE.D1.81.D0.BE.D0.B2_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82.D1.8B

        :param payment_type: Тип оплаты
        :param allow_change_payment: Вариант доступности изменения платежа
        :param state: Состояние
        :return:
        """
        if isinstance(allow_change_payment, str) and allow_change_payment not in self._Fields.allow_change_param:
            raise AbcpWrongParameterError(
                "allow_change_payment",
                allow_change_payment,
                f'Неверное значение параметра, допустимые значения {self._Fields.allow_change_param}')

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.PaymentMethods.METHODS_LIST, payload)


class Agreements:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @process_ts_dates('date_start', 'date_end')
    @ensure_list_params('contractor_ids', 'contractor_requisite_ids', 'shop_requisite_ids')
    @convert_bool_params_to_str('is_active', 'is_delete', 'is_default')
    async def get_list(self, contractor_ids: List | int | str = None,
                       contractor_requisite_ids: List | int | str = None,
                       shop_requisite_ids: List | int | str = None,
                       is_active: bool = None, is_delete: bool = None, is_default: bool = None,
                       agreement_type: int = None, relation_type: int = None,
                       number: str = None, currency: str = None,
                       date_start: str | datetime = None, date_end: str | datetime = None,
                       credit_limit: int | float = None,
                       limit: int = None, skip: int = None):
        """

        :param contractor_ids:
        :param contractor_requisite_ids:
        :param shop_requisite_ids:
        :param is_active:
        :param is_delete:
        :param is_default:
        :param agreement_type:
        :param relation_type:
        :param number:
        :param currency:
        :param date_start:
        :param date_end:
        :param credit_limit:
        :param limit:
        :param skip:
        :return:
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.Agreements.GET_LIST, payload)


class LegalPersons:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @check_limit
    @process_ts_lists('ids')
    async def get_list(self, ids: List | int | str = None, contractor_id: int | None = None,
                       form: int | None = None, org_type: int | None = None,
                       agreement_with_individuals_required: int | None = None,
                       with_tax_systems: int | None = None,
                       limit: int | None = None, offset: int | None = None):
        """

        :param ids:
        :param contractor_id:
        :param form:
        :param org_type:
        :param agreement_with_individuals_required:
        :param with_tax_systems:
        :param limit:
        :param offset:
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsAdmin.LegalPersons.GET_LIST, payload)


class SupplierOrders:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @check_limit
    @process_ts_dates('create_date_start', 'create_date_end', 'send_date_start', 'send_date_end')
    @process_ts_lists('orders_ids', 'distributor_ids', 'supplier_ids', 'send_statuses')
    async def orders_list(self, orders_ids: List | int | str = None,
                          distributor_ids: List | int | str = None,
                          supplier_ids: List | int | str = None,
                          send_statuses: List | int | str = None,
                          create_date_start: str | datetime = None,
                          create_date_end: str | datetime = None,
                          send_date_start: str | datetime = None,
                          send_date_end: str | datetime = None,
                          client_order_id: str | int = None,
                          client_order_number: str = None,
                          limit: str | int = None,
                          skip: str | int = None):
        """
        Получение списка заказов поставщикам

        :param orders_ids: список идентификаторов заказов
        :param distributor_ids: список идентификаторов прайс-листов
        :param supplier_ids: список идентификаторов поставщиков
        :param send_statuses: список статусов отправки
        :param create_date_start: начальная дата диапазона поиска по дате создания
        :param create_date_end: конечная дата диапазона поиска по дате создания
        :param send_date_start: начальная дата диапазона поиска по дате отправки
        :param send_date_end: конечная дата диапазона поиска по дате отправки
        :param client_order_id: идентификатор заказа клиента
        :param client_order_number: номер заказа клиента
        :param limit: максимальное количество заказов в ответе
        :param skip: количество заказов, которое нужно пропустить
        :return: список заказов поставщикам
        """
        payload = generate_payload(**locals())

        if isinstance(client_order_id, str) and not client_order_id.isdigit():
            raise AbcpWrongParameterError("client_order_id", client_order_id,
                                          "должен быть числом или строкой, содержащей число")

        return await self._base.request(_Methods.TsAdmin.SupplierOrders.ORDERS_LIST, payload, post=True)

    @check_limit
    @process_ts_dates('deadline_date_start', 'deadline_date_end')
    @process_ts_lists('statuses', 'distributor_ids', 'supplier_ids', 'position_ids', 'gr_position_ids')
    async def positions_list(self, statuses: List | str | int = None,
                             order_id: str | int = None,
                             distributor_ids: List | str | int = None,
                             supplier_ids: List | str | int = None,
                             position_ids: List | str | int = None,
                             gr_position_ids: List | str | int = None,
                             client_order_id: str | int = None,
                             client_order_number: str = None,
                             without_order: bool = None,
                             with_order: bool = None,
                             additional_info: List | str = None,
                             limit: str | int = None,
                             skip: str | int = None):
        """
        Получение списка позиций заказов поставщикам

        :param statuses: список статусов
        :param order_id: идентификатор заказа
        :param distributor_ids: список идентификаторов прайс-листов
        :param supplier_ids: список идентификаторов поставщиков
        :param position_ids: список идентификаторов позиций
        :param gr_position_ids: список идентификаторов позиций приходных операций
        :param client_order_id: идентификатор заказа клиента
        :param client_order_number: номер заказа клиента
        :param without_order: флаг без заказа
        :param with_order: флаг с заказом
        :param additional_info: дополнительная информация
        :param limit: максимальное количество позиций в ответе
        :param skip: количество позиций, которое нужно пропустить
        :return: список позиций заказов поставщикам
        """
        payload = generate_payload(**locals())

        if isinstance(client_order_id, str) and not client_order_id.isdigit():
            raise AbcpWrongParameterError(
                "client_order_id",
                client_order_id,
                "должен быть числом или строкой, содержащей число"
            )

        if isinstance(without_order, bool):
            payload['without_order'] = '1' if without_order else '0'
        if isinstance(with_order, bool):
            payload['with_order'] = '1' if with_order else '0'

        if additional_info is not None:
            payload["additional_info"] = check_fields(additional_info, ["items", "goodsReceipt"])

        return await self._base.request(_Methods.TsAdmin.SupplierOrders.POSITIONS_LIST, payload, post=True)


class TsAdminApi:
    """
    Администратор для TS API ABCP (API 2.0)

    Предоставляет доступ к API 2.0 для администраторов.
    """

    def __init__(self, base: BaseAbcp):
        """
        Инициализация API TS ABCP для администратора

        :param base: Объект с базовой конфигурацией API
        :type base: BaseAbcp
        """
        if not isinstance(base, BaseAbcp):
            raise AbcpWrongParameterError("base", base, "должен быть экземпляром BaseAbcp")
        self._base = base
        self._order_pickings: OrderPickings | None = None
        self._customer_complaints: CustomerComplaints | None = None
        self._supplier_returns: SupplierReturns | None = None
        self._distributor_owners: DistributorOwners | None = None
        self._orders: Orders | None = None
        self._cart: Cart | None = None
        self._positions: Positions | None = None
        self._good_receipts: GoodReceipts | None = None
        self._tags: Tags | None = None
        self._tags_relationships: TagsRelationships | None = None
        self._payments: Payments | None = None
        self._payment_methods: PaymentMethods | None = None
        self._agreements: Agreements | None = None
        self._legal_persons: LegalPersons | None = None
        self._supplier_orders: SupplierOrders | None = None

    @property
    def order_pickings(self) -> OrderPickings:
        """
        Получить доступ к API для операций отгрузки

        :return: Объект для работы с API отгрузок
        :rtype: OrderPickings
        """
        if self._order_pickings is None:
            self._order_pickings = OrderPickings(self._base)
        return self._order_pickings

    @property
    def customer_complaints(self) -> CustomerComplaints:
        """
        Получить доступ к API для операций рекламаций

        :return: Объект для работы с API рекламаций
        :rtype: CustomerComplaints
        """
        if self._customer_complaints is None:
            self._customer_complaints = CustomerComplaints(self._base)
        return self._customer_complaints

    @property
    def supplier_returns(self) -> SupplierReturns:
        """
        Получить доступ к API для операций возврата поставщику

        :return: Объект для работы с API возвратов поставщику
        :rtype: SupplierReturns
        """
        if self._supplier_returns is None:
            self._supplier_returns = SupplierReturns(self._base)
        return self._supplier_returns

    @property
    def distributor_owners(self) -> DistributorOwners:
        if self._distributor_owners is None:
            self._distributor_owners = DistributorOwners(self._base)
        return self._distributor_owners

    @property
    def orders(self) -> Orders:
        if self._orders is None:
            self._orders = Orders(self._base)
        return self._orders

    @property
    def cart(self) -> Cart:
        if self._cart is None:
            self._cart = Cart(self._base)
        return self._cart

    @property
    def positions(self) -> Positions:
        if self._positions is None:
            self._positions = Positions(self._base)
        return self._positions

    @property
    def good_receipts(self) -> GoodReceipts:
        if self._good_receipts is None:
            self._good_receipts = GoodReceipts(self._base)
        return self._good_receipts

    @property
    def tags(self) -> Tags:
        if self._tags is None:
            self._tags = Tags(self._base)
        return self._tags

    @property
    def tags_relationships(self) -> TagsRelationships:
        if self._tags_relationships is None:
            self._tags_relationships = TagsRelationships(self._base)
        return self._tags_relationships

    @property
    def payments(self) -> Payments:
        if self._payments is None:
            self._payments = Payments(self._base)
        return self._payments

    @property
    def payment_methods(self) -> PaymentMethods:
        if self._payment_methods is None:
            self._payment_methods = PaymentMethods(self._base)
        return self._payment_methods

    @property
    def agreements(self) -> Agreements:
        if self._agreements is None:
            self._agreements = Agreements(self._base)
        return self._agreements

    @property
    def legal_persons(self) -> LegalPersons:
        if self._legal_persons is None:
            self._legal_persons = LegalPersons(self._base)
        return self._legal_persons

    @property
    def supplier_orders(self) -> SupplierOrders:
        if self._supplier_orders is None:
            self._supplier_orders = SupplierOrders(self._base)
        return self._supplier_orders
