from datetime import datetime
from typing import Union, List, Dict, Optional, Any

from ..api import _Methods
from ..base import BaseAbcp
from ..exceptions import AbcpWrongParameterError
from ..utils.fields_checker import check_fields, check_limit, process_ts_dates, process_ts_lists
from ..utils.payload import generate_payload


class GoodReceipts:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def create(self, code: str | int,
                     positions: Union[List[Dict[str, str]], Dict[str, str]],
                     sup_number: str = None, sup_shipment_date: str | datetime = None):
        """
        Операция создания приёмки

        Source:
        :param code: Внутренний код контрагента-поставщика
        :param positions: список словарей с позициями
        :param sup_number: номер отгрузки поставщика
        :param sup_shipment_date: дата и время отгрузки поставщика <br> `str` в формате %Y-%m-%d %H:%M:%S или datetime object<br>
        :return: id `obj`
        """
        if isinstance(positions, dict):
            positions = [positions]
        payload = generate_payload(**locals())
        if isinstance(sup_shipment_date, datetime):
            payload["sup_shipment_date"] = f'{sup_shipment_date:%Y-%m-%d %H:%M:%S}'
        return await self._base.request(_Methods.TsClient.GoodReceipts.CREATE, payload, post=True)

    @check_limit
    @process_ts_dates('date_start', 'date_end')
    @process_ts_lists('statuses')
    async def get(self, limit: int = None, skip: int = None,
                  output: str = None,
                  auto: str = None,
                  creator_id: str | int = None, worker_id: str | int = None,
                  agreement_id: str | int = None, statuses: Union[List, str, int] = None,
                  number: str = None,
                  date_start: str | datetime = None, date_end: str | datetime = None,
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
        :param statuses: стататус или статусы в List (Возможные значения: от 1 до 3)
        :param number: номер операций
        :param date_start: начальная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param date_end: конечная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param sup_number:
        :return:
        """

        payload = generate_payload(**locals())
        if isinstance(output, str) and not all(x in 'des' for x in output):
            raise AbcpWrongParameterError("output", output, 'должен состоять из флагов "d", "e", "s"')

        return await self._base.request(_Methods.TsClient.GoodReceipts.GET, payload)

    @check_limit
    async def get_positions(self, op_id: str | int, limit: int = None, skip: int = None,
                            output: str = None, product_id: str | int = None, auto: str = None):
        """
        Получение списка позиций приёмки

        Source:

        :param op_id: идентификатор операции
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param skip: количество операций в ответе, которое нужно пропустить
        :param output: формат вывода, 'e' - загрузка дополнительной информации (справочные товары)
        :param product_id: идентификатор товара справочника
        :param auto:
        :return:
        """

        if isinstance(output, str) and output != 'e':
            raise AbcpWrongParameterError("output", output, 'может принимать только значение "e"')

        if isinstance(auto, str) and (len(auto) < 3):
            raise AbcpWrongParameterError("auto", auto, "должен состоять минимум из 3 символов")

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.GoodReceipts.GET_POSITIONS, payload)


class OrderPickings:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @check_limit
    @process_ts_dates('date_start', 'date_end')
    @process_ts_lists('status', 'co_old_pos_ids')
    async def get(self, limit: int = None, skip: int = None,
                  output: str = None, auto: str | int = None,
                  creator_id: str | int = None, worker_id: str | int = None,
                  agreement_id: str | int = None,
                  status: Union[List, str, int] = None, number: str = None,
                  date_start: str | datetime = None, date_end: str | datetime = None,
                  co_old_pos_ids: Union[List, str, int] = None):
        """
        Получение списка операций отгрузки (расход)

        Source:

        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param skip: количество операций в ответе, которое нужно пропустить
        :param output: формат вывода, флаг 'd' - загрузка удалённых операций, 'e' - загрузка дополнительной информации (договора), 's' - суммы по позициям, кол-во позиций
        :param auto: автоопределяемое поле (поиск по частичному номеру операции или идентификатору, если задано число)
        :param creator_id: идентификатор сотрудника-создателя
        :param worker_id: идентификатор сотрудника-исполнителя
        :param agreement_id: идентификатор договора
        :param status: статус или список статусов (От 1 до 3)
        :param number: номер операций
        :param date_start: начальная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param date_end: конечная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param co_old_pos_ids: список идентификаторов позиций старых заказов
        :return:
        """

        payload = generate_payload(**locals())

        if isinstance(status, int) and not 1 <= status <= 3:
            raise AbcpWrongParameterError("status", status, "должен быть в диапазоне от 1 до 3")

        if isinstance(output, str) and (not all(x in 'des' for x in output) or len(output) > 3):
            raise AbcpWrongParameterError("output", output, 'должен состоять из флагов "d", "e", "s"')

        return await self._base.request(_Methods.TsClient.OrderPickings.GET, payload)

    @check_limit
    async def get_positions(self, op_id: str | int, limit: int = None, skip: int = None, output: str = None,
                            product_id: str | int = None,
                            item_id: str | int = None, ignore_canceled: Union[int, bool] = None):
        """
        Получение списка позиций товаров отгрузки

        Source:

        :param op_id: идентификатор операции
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param skip: количество операций в ответе, которое нужно пропустить
        :param output: формат вывода, 'e' - загрузка дополнительной информации (справочные товары), 'o' - дополнительно вернуть инфу об операции
        :param product_id: идентификатор товара справочника
        :param item_id: идентификатор партии товара
        :param ignore_canceled: Признак не возвращать позиции аннулированных операций
        :return:
        """
        payload = generate_payload(**locals())

        if isinstance(ignore_canceled, bool):
            payload["ignore_canceled"] = 1 if ignore_canceled else None
        elif isinstance(ignore_canceled, int):
            if ignore_canceled == 0:
                payload["ignore_canceled"] = None
            elif ignore_canceled != 1:
                raise AbcpWrongParameterError(
                    "ignore_canceled", ignore_canceled, "должен быть 1 (True) или 0 (False)")

        if isinstance(output, str) and (not all(x in 'oe' for x in output) or len(output) > 2):
            raise AbcpWrongParameterError("output", output, 'должен состоять из флагов "o", "e"')

        return await self._base.request(_Methods.TsClient.OrderPickings.GET_POSITIONS, payload)


class CustomerComplaints:
    def __init__(self, base: BaseAbcp):
        self._base = base

    class FieldsChecker:
        get_fields = ["orderPicking", "agreement", "posInfo"]
        get_positions_fields = ["product", "orderPickingInfo", "operationInfo", "supplierReturnPos"]

    @check_limit
    @process_ts_dates('date_start', 'date_end')
    @process_ts_lists('position_statuses', 'tag_ids')
    async def get(self, auto: str | int = None, creator_id: str | int = None,
                  expert_id: str | int = None,
                  order_picking_id: str | int = None, position_statuses: Union[List, str, int] = None,
                  tag_ids: Union[List, str, int] = None, position_auto: str = None,
                  number: str = None, date_start: str | datetime = None, date_end: str | datetime = None,
                  skip: int = None, limit: int = None,
                  output: str = None, fields: Union[List, str] = None):
        """
        Получение списка операций рекламаций

        Source:

        :param auto: автоопределяемое поле (поиск по частичному номеру операции или идентификатору, если задано число)
        :param creator_id: идентификатор сотрудника-создателя
        :param expert_id: идентификатор сотрудника-эксперта
        :param order_picking_id: идентификатор операции отгрузки, по которой создана рекламация
        :param position_statuses: список статусов позиций (Возможные значения: 0, 1, 2)
        :param tag_ids: список идентификаторов тегов
        :param position_auto: автоопределяемое поле для поиска по позициям
        :param number: номер операции
        :param date_start: начальная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param date_end: конечная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param skip: количество операций в ответе, которое нужно пропустить
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param output: формат вывода
        :param fields: дополнительные поля для вывода (orderPicking, agreement, posInfo)
        :return:
        """

        payload = generate_payload(**locals())

        if fields is not None:
            payload["fields"] = check_fields(fields, self.FieldsChecker.get_fields)

        return await self._base.request(_Methods.TsClient.CustomerComplaints.GET, payload)

    @check_limit
    @process_ts_dates('date_start', 'date_end')
    @process_ts_lists('order_picking_good_ids', 'picking_ids', 'old_co_position_ids')
    async def get_positions(self, op_id: str | int,
                            order_picking_good_id: str | int = None,
                            order_picking_good_ids: Union[List, str, int] = None,
                            picking_ids: Union[List, str, int] = None,
                            old_co_position_ids: Union[List, str, int] = None,
                            old_item_id: str | int = None,
                            item_id: str | int = None, loc_id: str | int = None,
                            status: int = None, date_start: str | datetime = None,
                            date_end: str | datetime = None,
                            type: str | int = None, skip: int = None, limit: int = None,
                            output: str = None, fields: Union[List, str] = None
                            ):
        """
        Получение списка позиций рекламаций

        Source:

        :param op_id: идентификатор операции
        :param order_picking_good_id: идентификатор позиции отгрузки
        :param order_picking_good_ids: список идентификаторов позиций отгрузки
        :param picking_ids: список идентификаторов операций отгрузки
        :param old_co_position_ids: список идентификаторов позиций старых заказов клиента
        :param old_item_id: идентификатор старой партии
        :param item_id: идентификатор партии
        :param loc_id: идентификатор склада
        :param status: статус позиции (Возможные значения: 0, 1, 2)
        :param date_start: начальная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param date_end: конечная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param type: тип позиций (Возможные значения: 0 - принятые, 1 - на доработке, 2 - отклонённые)
        :param skip: количество операций в ответе, которое нужно пропустить
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param output: формат вывода
        :param fields: дополнительные поля
        :return:
        """

        payload = generate_payload(**locals())

        if fields is not None:
            payload["fields"] = check_fields(fields, self.FieldsChecker.get_positions_fields)

        return await self._base.request(_Methods.TsClient.CustomerComplaints.GET_POSITIONS, payload)

    async def create(self, order_picking_id: str | int, positions: Union[List[Dict], Dict]):
        """
        Создание рекламации

        Source:

        :param order_picking_id: идентификатор операции отгрузки
        :param positions: список позиций или одна позиция
        :return: id рекламации
        """
        if isinstance(positions, dict):
            positions = [positions]

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.CustomerComplaints.CREATE, payload, post=True)

    async def create_position_multiple(self, positions: Union[List[Dict], Dict],
                                       customer_complaint_id: int,
                                       customer_complaint: str,
                                       custom_complaint_file: str = None):
        """
        Создание позиций рекламаций

        Source:

        :param positions: список позиций или одна позиция
        :param customer_complaint_id: идентификатор рекламации
        :param customer_complaint: комментарий к рекламации
        :param custom_complaint_file: файл рекламации в base64
        :return: результат операции
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.CustomerComplaints.CREATE_POSITION_MULTIPLE, payload,
                                        post=True)

    async def update_position(self, id: int, quantity: str | int):
        """
        Изменение позиции рекламации

        Source:

        :param id: идентификатор позиции
        :param quantity: новое количество
        :return: результат операции
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.CustomerComplaints.UPDATE, payload, post=True)

    async def cancel_position(self, id: int):
        """
        Отмена позиции рекламации

        Source:

        :param id: идентификатор позиции
        :return: результат операции
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.CustomerComplaints.CANCEL, payload, post=True)


class Orders:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @process_ts_dates('create_time')
    @process_ts_lists('positions')
    async def create_by_cart(self, delivery_address: str, delivery_person: str, delivery_contact: str,
                             delivery_comment: str = None, delivery_method_id: str | int = None,
                             number: str | int = None, create_time: str | datetime = None,
                             positions: Union[List, str, int] = None):
        """
        Создание заказа по содержимому корзины

        Source:

        :param delivery_address: адрес доставки
        :param delivery_person: контактное лицо
        :param delivery_contact: контактный телефон
        :param delivery_comment: комментарий к доставке
        :param delivery_method_id: идентификатор типа доставки
        :param number: номер заказа
        :param create_time: дата и время создания
        :param positions: список позиций корзины для заказа
        :return: идентификатор заказа
        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.TsClient.Orders.CREATE, payload, post=True)

    @check_limit
    @process_ts_dates('date_start', 'date_end',
                      'update_date_start', 'update_date_end',
                      'deadline_date_start', 'deadline_date_end')
    @process_ts_lists('order_ids', 'product_ids', 'position_statuses')
    async def get_list(self, number: str | int = None, agreement_id: str | int = None,
                       manager_id: str | int = None,
                       delivery_id: str | int = None, brand: str = None, message: str = None,
                       date_start: str | datetime = None, date_end: str | datetime = None,
                       update_date_start: str | datetime = None, update_date_end: str | datetime = None,
                       deadline_date_start: str | datetime = None,
                       deadline_date_end: str | datetime = None,
                       order_ids: Union[List, str, int] = None,
                       product_ids: Union[List, str, int] = None,
                       position_statuses: Union[List, str, int] = None, limit: int = None,
                       skip: int = None):
        """
        Получение списка заказов

        Source:

        :param number: номер заказа
        :param agreement_id: идентификатор договора
        :param manager_id: идентификатор менеджера
        :param delivery_id: идентификатор доставки
        :param brand: бренд
        :param message: сообщение
        :param date_start: начальная дата диапазона поиска
        :param date_end: конечная дата диапазона поиска
        :param update_date_start: начальная дата диапазона поиска по обновлению
        :param update_date_end: конечная дата диапазона поиска по обновлению
        :param deadline_date_start: начальная дата диапазона поиска по сроку
        :param deadline_date_end: конечная дата диапазона поиска по сроку
        :param order_ids: список идентификаторов заказов
        :param product_ids: список идентификаторов товаров
        :param position_statuses: список статусов позиций
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000.
        :param skip: количество операций в ответе, которое нужно пропустить
        :return: список заказов
        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.TsClient.Orders.GET_LIST, payload)

    async def get_order(self, order_id: str | int):
        """
        Получение заказа

        Source:

        :param order_id: идентификатор заказа
        :return: данные заказа
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.Orders.GET, payload)

    async def refuse(self, order_id: str | int):
        """
        Отказ от заказа

        Source:

        :param order_id: идентификатор заказа
        :return: результат операции
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.Orders.REFUSE, payload, post=True)


class Cart:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def create(self, brand: str, number: str, quantity: int, supplier_code: str | int, item_key: str,
                     agreement_id: str | int = None) -> Dict[str, Any]:
        """
        Создание позиции в корзине

        Source:

        :param brand: бренд
        :param number: артикул
        :param quantity: количество
        :param supplier_code: код поставщика
        :param item_key: ключ товара
        :param agreement_id: идентификатор договора
        :return: данные позиции
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.Cart.CREATE, payload, post=True)

    async def update(self, position_id: str | int, quantity: int):
        """
        Обновление позиции в корзине

        Source:

        :param position_id: идентификатор позиции
        :param quantity: количество
        :return: результат операции
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.Cart.UPDATE, payload, post=True)

    @check_limit
    @process_ts_lists('position_ids')
    async def get_list(self, position_ids: Union[List, str, int] = None, agreement_id: str | int = None,
                       limit: int = None,
                       skip: int = None) -> List[Dict[str, Any]]:
        """
        Получение списка позиций в корзине

        Source:

        :param position_ids: список идентификаторов позиций
        :param agreement_id: идентификатор договора
        :param limit: максимальное количество позиций в ответе
        :param skip: количество позиций, которое нужно пропустить
        :return: список позиций
        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.TsClient.Cart.GET_LIST, payload)

    async def exist(self, agreement_id: str | int, brand: str, number_fix: str):
        """
        Проверка наличия товара в корзине

        Source:

        :param agreement_id: идентификатор договора
        :param brand: бренд
        :param number_fix: артикул
        :return: результат проверки
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.Cart.EXIST, payload)

    async def summary(self, agreement_id: str | int = None):
        """
        Получение сводной информации по корзине

        Source:

        :param agreement_id: идентификатор договора
        :return: сводная информация
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.Cart.SUMMARY, payload)

    async def clear(self, agreement_id: str | int):
        """
        Очистка корзины

        Source:

        :param agreement_id: идентификатор договора
        :return: результат операции
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.TsClient.Cart.CLEAR, payload, post=True)

    @process_ts_lists('position_ids')
    async def delete_positions(self, position_ids: Union[List, str, int]):
        """
        Удаление позиций из корзины

        Source:

        :param position_ids: список идентификаторов позиций
        :return: результат операции
        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.TsClient.Cart.DELETE, payload, post=True)


class Positions:
    def __init__(self, base: BaseAbcp):
        self._base = base

    class FieldsChecker:
        additional_info = ["delivery", "unpaidAmount"]
        statuses = ["prepayment", "canceled", "new",
                    "ordered", "refused", "confirm",
                    "done", "closed"]

    async def get_position(self, position_id: str | int, additional_info: Union[List, str] = None):
        """
        Получение позиции

        Source:

        :param position_id: идентификатор позиции
        :param additional_info: дополнительная информация
        :return: данные позиции
        """
        payload = generate_payload(**locals())

        if additional_info is not None:
            payload["additional_info"] = check_fields(additional_info, self.FieldsChecker.additional_info)

        return await self._base.request(_Methods.TsClient.Positions.GET, payload)

    @check_limit
    @process_ts_dates('date_start', 'date_end',
                      'update_date_start', 'update_date_end',
                      'deadline_date_start', 'deadline_date_end')
    @process_ts_lists('route_ids', 'distributor_ids',
                      'ids', 'order_ids', 'product_ids', 'statuses', 'tag_ids', 'statuses')
    async def get_list(self, brand: str = None, message: str = None, agreement_id: str | int = None,
                       manager_id: str | int = None,
                       no_manager_assigned: bool = False,
                       date_start: str | datetime = None, date_end: str | datetime = None,
                       update_date_start: str | datetime = None, update_date_end: str | datetime = None,
                       deadline_date_start: str | datetime = None, deadline_date_end: str | datetime = None,
                       route_ids: Union[List, str, int] = None,
                       distributor_ids: Union[List, str, int] = None, ids: Union[List, str, int] = None,
                       order_ids: Union[List, str, int] = None, product_ids: Union[List, str, int] = None,
                       statuses: Union[List, str] = None,
                       tag_ids: Union[List, str, int] = None,
                       limit: int = None, skip: int = None,
                       additional_info: Union[List, str] = None):
        """
        Получение списка позиций заказов

        Source:

        :param brand: бренд
        :param message: сообщение
        :param agreement_id: идентификатор договора
        :param manager_id: идентификатор менеджера
        :param no_manager_assigned: флаг отсутствия менеджера
        :param date_start: начальная дата диапазона поиска по дате создания
        :param date_end: конечная дата диапазона поиска по дате создания
        :param update_date_start: начальная дата диапазона поиска по дате обновления
        :param update_date_end: конечная дата диапазона поиска по дате обновления
        :param deadline_date_start: начальная дата диапазона поиска по сроку
        :param deadline_date_end: конечная дата диапазона поиска по сроку
        :param route_ids: список идентификаторов маршрутов
        :param distributor_ids: список идентификаторов дистрибьюторов
        :param ids: список идентификаторов позиций
        :param order_ids: список идентификаторов заказов
        :param product_ids: список идентификаторов товаров
        :param statuses: список статусов
        :param tag_ids: список идентификаторов тегов
        :param limit: максимальное количество позиций в ответе
        :param skip: количество позиций, которое нужно пропустить
        :param additional_info: дополнительная информация
        :return: список позиций
        """
        payload = generate_payload(**locals())

        if additional_info is not None:
            payload["additional_info"] = check_fields(additional_info, self.FieldsChecker.additional_info)

        return await self._base.request(_Methods.TsClient.Positions.GET_LIST, payload)

    async def cancel(self, position_id: str | int, additional_info: Union[List, str] = None):
        """
        Отказ от позиции заказа

        Source:

        :param position_id: идентификатор позиции
        :param additional_info: дополнительная информация
        :return: результат операции
        """
        payload = generate_payload(**locals())

        if additional_info is not None:
            payload["additional_info"] = check_fields(additional_info, self.FieldsChecker.additional_info)

        return await self._base.request(_Methods.TsClient.Positions.CANCEL, payload, post=True)

    @process_ts_lists('position_ids')
    async def mass_cancel(self, position_ids: Union[List, str, int], additional_info: Union[List, str] = None):
        """
        Массовый отказ от позиций заказов

        Source:

        :param position_ids: список идентификаторов позиций
        :param additional_info: дополнительная информация
        :return: результат операции
        """
        payload = generate_payload(**locals())

        if additional_info is not None:
            payload["additional_info"] = check_fields(additional_info, self.FieldsChecker.additional_info)

        return await self._base.request(_Methods.TsClient.Positions.MASS_CANCEL, payload, post=True)


class Agreements:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @check_limit
    @process_ts_dates('date_start', 'date_end')
    @process_ts_lists('contractor_ids', 'contractor_requisite_ids', 'shop_requisite_ids')
    async def get_list(self, contractor_ids: Union[int, str, List[int]] = None,
                       contractor_requisite_ids: Union[int, str, List[int]] = None,
                       shop_requisite_ids: Union[int, str, List[int]] = None,
                       is_active: bool = None, is_delete: bool = None, is_default: bool = None,
                       agreement_type: int = None, relation_type: int = None,
                       number: str = None, currency: str = None,
                       date_start: str | datetime = None, date_end: str | datetime = None,
                       credit_limit: Union[float, int] = None,
                       limit: int = None, skip: int = None):
        """
        Получение списка договоров

        Source:

        :param contractor_ids: идентификатор или список идентификаторов контрагентов
        :param contractor_requisite_ids: идентификатор или список идентификаторов реквизитов контрагентов
        :param shop_requisite_ids: идентификатор или список идентификаторов реквизитов магазина
        :param is_active: флаг активности
        :param is_delete: флаг удаления
        :param is_default: флаг "по умолчанию"
        :param agreement_type: тип договора
        :param relation_type: тип отношений
        :param number: номер договора
        :param currency: валюта
        :param date_start: начальная дата договора
        :param date_end: конечная дата договора
        :param credit_limit: кредитный лимит
        :param limit: максимальное количество договоров в ответе
        :param skip: количество договоров, которое нужно пропустить
        :return: список договоров
        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.TsClient.Agreements.GET_LIST, payload)


class TsClientApi:
    """
    Клиент для TS API ABCP (API 2.0)
    
    Предоставляет доступ к API 2.0 для клиентов.
    """

    def __init__(self, base: BaseAbcp):
        """
        Инициализация API TS ABCP
        
        :param base: Объект с базовой конфигурацией API
        :type base: BaseAbcp
        """
        if not isinstance(base, BaseAbcp):
            raise AbcpWrongParameterError("base", base, "должен быть экземпляром BaseAbcp")
        self._base = base
        self._good_receipts: Optional[GoodReceipts] = None
        self._order_pickings = None
        self._customer_complaints = None
        self._orders = None
        self._cart = None
        self._positions = None
        self._agreements = None

    @property
    def good_receipts(self) -> GoodReceipts:
        """
        Получить доступ к API для операций c приёмками
        
        :return: Объект для работы с API приёмок
        :rtype: GoodReceipts
        """
        if self._good_receipts is None:
            self._good_receipts = GoodReceipts(self._base)
        return self._good_receipts

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
    def orders(self) -> Orders:
        """
        Получить доступ к API для операций заказов
        
        :return: Объект для работы с API заказов
        :rtype: Orders
        """
        if self._orders is None:
            self._orders = Orders(self._base)
        return self._orders

    @property
    def cart(self) -> Cart:
        """
        Получить доступ к API для операций корзины
        
        :return: Объект для работы с API корзины
        :rtype: Cart
        """
        if self._cart is None:
            self._cart = Cart(self._base)
        return self._cart

    @property
    def positions(self) -> Positions:
        """
        Получить доступ к API для операций позиций заказов
        
        :return: Объект для работы с API позиций заказов
        :rtype: Positions
        """
        if self._positions is None:
            self._positions = Positions(self._base)
        return self._positions

    @property
    def agreements(self) -> Agreements:
        """
        Получить доступ к API для операций договоров
        
        :return: Объект для работы с API договоров
        :rtype: Agreements
        """
        if self._agreements is None:
            self._agreements = Agreements(self._base)
        return self._agreements
