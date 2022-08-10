import logging
from datetime import datetime
from types import NoneType
from typing import Union, List, Dict

import pytz
from pyrfc3339 import generate

from .. import api
from ..base import BaseAbcp
from ..exceptions import AbcpWrongParameterError
from ..utils.fields_checker import check_fields
from ..utils.payload import generate_payload

logger = logging.getLogger('Ts.Client')


class GoodReceipts(BaseAbcp):
    async def create(self, code: Union[str, int],
                     positions: Union[List[Dict[str, str]], Dict[str, str]],
                     sup_number: str = None, sup_shipment_date: Union[str, datetime] = None):
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
            sup_shipment_date = f'{sup_shipment_date:%Y-%m-%d %H:%M:%S}'
        return await self.request(api.Methods.TsClient.GoodReceipts.CREATE, payload, True)

    async def get(self, limit: int = None, skip: int = None,
                  output: str = None,
                  auto: str = None,
                  creator_id: Union[int, str] = None, worker_id: Union[int, str] = None,
                  agreement_id: Union[int, str] = None, statuses: Union[List, str, int] = None,
                  number: str = None,
                  date_start: Union[str, datetime] = None, date_end: Union[str, datetime] = None,
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
        if isinstance(limit, int) and not (1 <= limit <= 1000):
            raise AbcpWrongParameterError('Параметр "limit" может принимать значения от 1 до 1000')
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(output, str) and not all(x in 'des' for x in output):
            raise AbcpWrongParameterError('Параметр "output" должен состоять из  ["d", "e", "s"]')
        if isinstance(statuses, list):
            if all(1 <= int(x) <= 3 for x in statuses):
                statuses = ','.join(map(str, statuses))
            else:
                raise AbcpWrongParameterError('Параметр "statuses" принимет значения от 1 до 3')
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.GoodReceipts.GET, payload)

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
        :param auto:
        :return:
        """
        if isinstance(limit, int) and not (1 <= limit <= 1000):
            raise AbcpWrongParameterError('Параметр "limit" может принимать значения от 1 до 1000')
        if isinstance(output, str) and output != 'e':
            raise AbcpWrongParameterError('Параметр "output" принимает только значение "e"')
        if isinstance(auto, str) and (len(auto) < 3):
            raise AbcpWrongParameterError('Параметр "auto" должен состоять минимум из 3 символов')
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.GoodReceipts.GET_POSITIONS, payload)


class OrderPickings(BaseAbcp):
    async def get(self, limit: int = None, skip: int = None,
                  output: str = None, auto: Union[str, int] = None,
                  creator_id: Union[int, str] = None, worker_id: Union[int, str] = None, agreement_id: Union[int, str] = None,
                  status: Union[List, str, int] = None, number: str = None,
                  date_start: Union[str, datetime] = None, date_end: Union[str, datetime] = None,
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
        if isinstance(limit, int) and not (1 <= limit <= 1000):
            raise AbcpWrongParameterError('Параметр "limit" может принимать значения от 1 до 1000')
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(status, int) and not (1 <= status <= 3):
            raise AbcpWrongParameterError('Параметр "status" принимет значения от 1 до 3')
        if isinstance(status, list):
            if all(1 <= x <= 3 for x in status):
                statuses = ','.join(map(str, status))
            else:
                raise AbcpWrongParameterError('Параметр "status" принимет значения от 1 до 3')
        if isinstance(output, str) and (not all(x in 'des' for x in output) or len(output) > 3):
            raise AbcpWrongParameterError('Параметр "output" должен состоять из  ["d", "e", "s"]')
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.OrderPickings.GET, payload)

    async def get_positions(self, op_id: Union[str, int], limit: int = None, skip: int = None, output: str = None,
                            product_id: Union[int, str] = None,
                            item_id: Union[int, str] = None, ignore_canceled: Union[int, bool] = None):
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

        if isinstance(output, str) and (not all(x in 'oe' for x in output) or len(output) > 2):
            raise AbcpWrongParameterError('Параметр "output" должен состоять из  ["o", "e"]')
        elif not isinstance(output, NoneType):
            raise AbcpWrongParameterError('output must be a string')
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.OrderPickings.GET_POSITIONS, payload)


class CustomerComplaints(BaseAbcp):
    class FieldsChecker:
        get_fields = ["orderPicking", "agreement", "posInfo"]
        get_positions_fields = ["product", "orderPickingInfo", "operationInfo", "supplierReturnPos"]

    async def get(self, auto: Union[str, int] = None, creator_id: Union[int, str] = None, expert_id: Union[int, str] = None,
                  order_picking_id: Union[int, str] = None, position_statuses: Union[List, str, int] = None,
                  tag_ids: Union[List,str, int] = None, position_auto: str = None,
                  number: str = None, date_start: Union[str, datetime] = None, date_end: Union[str, datetime] = None,
                  skip: int = None, limit: int = None,
                  output: str = None, fields: Union[List, str] = None):
        # Who choose this namespacing with camelCase, snake_case, wtf case like tagIDs?

        """
        Получение списка операций возврата покупателя

        Source:

        :param auto: автоопределяемое поле (поиск по частичному номеру операции или идентификатору, если задано число)
        :param creator_id: идентификатор сотрудника-создателя
        :param expert_id: идентификатор сотрудника-эксперта
        :param order_picking_id: идентификатор отгрузки
        :param position_statuses: массив статусов позиций
        :param tag_ids: массив идентификаторов тегов
        :param position_auto: автоопределяемый параметр для поиска по позициям операции
        :param number: номер операции
        :param date_start: начальная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param date_end:  конечная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param skip: количество операций в ответе, которое нужно пропустить
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param output: формат вывода, 'e' - загрузка дополнительной информации(операция отгрузки и договор), 's' - будет возвращена дополнительная информация о количестве позиций во всех возможных статусах.
        :param fields: загрузка дополнительной информации. Строка со следующими параметрами через запятую:<br><br>
                    orderPicking - операция отгрузки, по которой создан возврат<br>
                    agreement - договор, по которому выполнена отгрузка<br>
                    posInfo - информация о количестве позиций во всех возможных статусах
        :return:
        """
        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(tag_ids, int) or isinstance(tag_ids, str):
            tag_ids = [tag_ids]
        if isinstance(position_statuses, list):
            position_statuses = ','.join(map(str, position_statuses))
        if not isinstance(fields, NoneType):
            fields = check_fields(fields, self.FieldsChecker.get_fields)
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.CustomerComplaints.GET, payload)

    async def get_positions(self, op_id: Union[str, int],
                            order_picking_good_id: Union[int, str] = None,
                            order_picking_good_ids: Union[List, str, int] = None,
                            picking_ids: Union[List, str, int] = None,
                            old_co_position_ids: Union[List, str, int] = None,
                            old_item_id: Union[int, str] = None,
                            item_id: Union[int, str] = None, loc_id: Union[int, str] = None,
                            status: int = None, date_start: Union[str, datetime] = None,
                            date_end: Union[str, datetime] = None,
                            type: Union[str, int] = None, skip: int = None, limit: int = None,
                            output: str = None, fields: Union[List, str] = None
                            ):
        """
        Получение списка позиций возврата покупателя

        Source:

        :param op_id: идентификатор операции
        :param order_picking_good_id: идентификатор позиции отгрузки
        :param order_picking_good_ids: идентификаторы позиций расхода через запятую
        :param picking_ids:  идентификаторы операции расхода через запятую
        :param old_co_position_ids: Идентификаторы позиции заказа через запятую.
        :param old_item_id: идентификатор партии из отгрузки
        :param item_id: идентификатор созданной партии
        :param loc_id: идентификатор места хранения
        :param status:  статус позиции (1 - новый, 2 - в работе, 3 - отказ, 4 - подтверждён, 5 - выдано, 6 - аннулировано)
        :param date_start: Начальная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param date_end: Конечная дата диапазона поиска `str` в формате RFC3339 или datetime object
        :param type:тип возврата (1 - возврат, 2 - отказ, 3 - брак.)
        :param skip: количество операций в ответе, которое нужно пропустить
        :param limit: максимальное количество операций, которое должно быть возвращено в ответе. Максимально возможное значение 1000. Если не указан будет установлено максимально возможное значение.
        :param output:  формат вывода, 'e' - загрузка дополнительной информации (справочные товары)
        :param fields: # TODO Check parameters contains only ['orderPickingInfo', 'product', 'operationInfo', 'supplierReturnPos]
        :return:
        """
        if isinstance(order_picking_good_ids, list):
            order_picking_good_ids = ','.join(map(str, order_picking_good_ids))

        if isinstance(picking_ids, list):
            picking_ids = ','.join(map(str, picking_ids))

        if isinstance(old_co_position_ids, list):
            old_co_position_ids = ','.join(map(str, old_co_position_ids))

        if isinstance(date_start, datetime):
            date_start = generate(date_start.replace(tzinfo=pytz.utc))
        if isinstance(date_end, datetime):
            date_end = generate(date_end.replace(tzinfo=pytz.utc))
        if isinstance(status, int) and not (1 <= status <= 6):
            raise AbcpWrongParameterError('Параметр "status" должен быть в диапазоне от 1 до 6')
        if isinstance(type, int) and not (1 <= type <= 3):
            raise AbcpWrongParameterError('Параметр "type" должен быть в диапазоне от 1 до 3')
        if isinstance(output, str) and output != 'e':
            raise AbcpWrongParameterError('Параметр "output" принимает только значение "e"')
        if not isinstance(fields, NoneType):
            fields = check_fields(fields, self.FieldsChecker.get_positions_fields)

        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.CustomerComplaints.GET_POSITIONS, payload)

    async def create(self, order_picking_id: Union[str, int], positions: Union[List[Dict], Dict]):
        """
        Создание возврата покупателя

        Source:

        :param order_picking_id: идентификатор отгрузки из которой возвращается товар
        :param positions: список позиций
        :return:
        """

        if isinstance(positions, dict):
            positions = [positions]
        payload = generate_payload(exclude=['positions'], **locals())
        return await self.request(api.Methods.TsClient.CustomerComplaints.CREATE, payload, True)

    async def update_position(self, id: int, quantity: Union[str, int]):
        """
        Изменение позиции возврата покупателя

        Возможно изменение только количества товара позиции. Изменение возможно только в статусе "новый".

        Source:

        :param id: идентификатор позиции возврата покупателя
        :param quantity: количество
        :return:
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.CustomerComplaints.UPDATE, payload, True)

    async def cancel_position(self, id: int):
        """
        Отмена позиции возврата покупателя

        Отмена позиции возможна только в статусе "новый". Отмена позиции происходит путём изменения статуса позиции в статус 6 - аннулировано.

        Source:

        :param id: идентификатор позиции возврата покупателя

        :return:
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.CustomerComplaints.CANCEL, payload, True)


class Orders(BaseAbcp):
    async def create_by_cart(self, delivery_address: str, delivery_person: str, delivery_contact: str,
                             delivery_comment: str = None, delivery_method_id: Union[int, str] = None,
                             number: Union[str, int] = None, create_time: Union[str, datetime] = None,
                             positions: Union[List,str, int] = None):
        """

        :param delivery_address: адрес доставки
        :param delivery_person: контактное лицо
        :param delivery_contact: контакт(телефон) получателя
        :param delivery_comment: комментарий
        :param delivery_method_id: ID способа доставки
        :param number: номер заказа, если не указан, то сформируется согласно шаблону номеров заказов, если указан, то проверяется на уникальность
        :param create_time: дата и время создания заказа, если не указан, заполняется автоматически, не может быть из будущего. `str` в формате RFC3339 или datetime object
        :param positions: список ID позиций корзины
        :return:
        """
        if isinstance(create_time, datetime):
            create_time = generate(create_time.replace(tzinfo=pytz.utc))
        if isinstance(positions, int) or isinstance(positions, str):
            positions = [positions]
        payload = generate_payload(
            exclude=['delivery_address', 'delivery_person',
                     'delivery_contact', 'delivery_comment', 'delivery_method_id'],
            **locals())
        return await self.request(api.Methods.TsClient.Orders.CREATE, payload, True)

    async def get_list(self, number: Union[str, int] = None, agreement_id: Union[int, str] = None,
                       manager_id: Union[int, str] = None,
                       delivery_id: Union[int, str] = None, brand: str = None, message: str = None,
                       date_start: Union[str, datetime] = None, date_end: Union[str, datetime] = None,
                       update_date_start: Union[str, datetime] = None, update_date_end: Union[str, datetime] = None,
                       deadline_date_start: Union[str, datetime] = None,
                       deadline_date_end: Union[str, datetime] = None,
                       order_ids: Union[List, str, int] = None,
                       product_ids: Union[List, str, int] = None,
                       position_statuses: Union[List, str, int] = None, limit: int = None,
                       skip: int = None):
        """

        :param number: номер заказа
        :param agreement_id: Идентификатор соглашения
        :param manager_id: Идентификатор менеджера
        :param delivery_id: Идентификатор доставки
        :param brand: бренд товара, полное совпадение
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
        return await self.request(api.Methods.TsClient.Orders.GET_LIST, payload)

    async def get_order(self, order_id: Union[str, int]):
        """
        Получение одного заказа

        Source:

        :param order_id: Идентификатор заказа.
        :return:
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Orders.GET, payload)

    async def refuse(self, order_id: Union[str, int]):
        """
        Отказ от заказа

        Source:

        :param order_id:
        :return:
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Orders.REFUSE, payload, True)


class Cart(BaseAbcp):
    async def create(self, brand: str, number: str, quantity: int, supplier_code: Union[str, int], item_key: str,
                     agreement_id: Union[int, str] = None):
        """
        Добавление позиции в корзину

        Source:

        :param brand: бренд
        :param number: артикул по стандарту ABCP
        :param quantity: количество товара
        :param supplier_code: идентификатор маршрута прайс-листа
        :param item_key: Код товара, полученный поиском search/articles | await api.cp.client.search.articles(602000600, 'Luk')
        :param agreement_id: идентификатор договора, если не указан, то используется активный договор с клиентом по умолчанию
        :return:
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Cart.CREATE, payload, True)

    async def update(self, position_id: Union[str, int], quantity: int):
        """
        Обновление позиции в корзине

        Source:

        :param position_id: идентификатор позиции в корзине
        :param quantity: новое количество
        :return:
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Cart.UPDATE, payload, True)

    async def get_list(self, position_ids: Union[List, str, int] = None, agreement_id: Union[int, str] = None,
                       limit: int = None,
                       skip: int = None):
        """
        Получение списка позиций в корзине

        Source:
        :param position_ids: Список идентификаторов позиций в корзине, через запятую
        :param agreement_id: идентификатор договора, если не указан, то используется активный договор с клиентом по умолчанию
        :param limit: максимальное количество позиций корзины, которое должно быть возвращено в ответе
        :param skip: количество позиций корзины в ответе, которое нужно пропустить
        :return:
        """
        if isinstance(position_ids, list):
            position_ids = ','.join(map(str, position_ids))
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Cart.GET_LIST, payload, True)

    async def exist(self, agreement_id: Union[str, int], brand: str, number_fix: str):
        """
        Проверка наличия позиции в корзине

        Source:

        :param agreement_id: идентификатор договора
        :param brand: бренд
        :param number_fix: артикул по стандарту ABCP
        :return:
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Cart.EXIST, payload)

    async def summary(self, agreement_id: Union[int, str] = None):
        """
        Получение суммарной информации по позициям корзины

        Source:
        :param agreement_id: идентификатор договора, если не указан, то используется активный договор с клиентом по умолчанию
        :return:
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Cart.SUMMARY, payload)

    async def clear(self, agreement_id: Union[str, int]):
        """
        Очистка корзины выбранного договора

        Source:
        :param agreement_id: идентификатор договора
        :return:
        """
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Cart.CLEAR, payload, True)

    async def delete_positions(self, position_ids: Union[List,str, int]):
        """
        Удаление позиций корзины

        Source:
        :param position_ids:
        :return:
        """
        if isinstance(position_ids, int) or isinstance(position_ids, str):
            position_ids = [position_ids]

        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Cart.DELETE, payload, True)


class Positions(BaseAbcp):
    class FieldsChecker:
        additional_info = ["delivery", "unpaidAmount"]
        statuses = ["prepayment", "canceled", "new",
                    "supOrder", "supOrderCanceled", "reservation",
                    "orderPicking", "delivery", "finished"]

    async def get_position(self, position_id: Union[str, int], additional_info: Union[List, str] = None):
        """

        :param position_id: идентификатор позиции заказа
        :param additional_info: доп. информация. Значения `str` или List ["delivery", "unpaidAmount"]
        :return:
        """
        if not isinstance(additional_info, NoneType):
            additional_info = check_fields(additional_info, self.FieldsChecker.additional_info)
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Positions.GET, payload)

    async def get_list(self, brand: str = None, message: str = None, agreement_id: Union[int, str] = None, manager_id: Union[int, str] = None,
                       no_manager_assigned: bool = False,
                       date_start: Union[str, datetime] = None, date_end: Union[str, datetime] = None,
                       update_date_start: Union[str, datetime] = None, update_date_end: Union[str, datetime] = None,
                       deadline_date_start: Union[str, datetime] = None, deadline_date_end: Union[str, datetime] = None,
                       route_ids: Union[List, str, int] = None,
                       distributor_ids: Union[List,str, int] = None, ids: Union[List, str, int] = None,
                       order_ids: Union[List, str, int] = None, product_ids: Union[List, str, int] = None,
                       statuses: Union[List, str] = None,
                       tag_ids: Union[List, str, int] = None,
                       limit: int = None, skip: int = None,
                       additional_info: Union[List, str] = None):
        """


        :param brand:  бренд товара, полное совпадение
        :param message: комментарий к позиции
        :param agreement_id: идентификатор соглашения
        :param manager_id: идентификатор менеджера
        :param no_manager_assigned: добавляющий в выборку позиции без назначенного менеджера; используется с managerId
        :param date_start: минимальная дата создания позиций заказов `str` в формате RFC3339 или datetime object
        :param date_end: максимальная дата создания позиций заказов `str` в формате RFC3339 или datetime object
        :param update_date_start: минимальная дата обновления заказов `str` в формате RFC3339 или datetime object
        :param update_date_end: максимальная дата обновления заказов `str` в формате RFC3339 или datetime object
        :param deadline_date_start: минимальная дата ожидаемая дата поставки на склад `str` в формате RFC3339 или datetime object
        :param deadline_date_end: максимальная дата ожидаемая дата поставки на склад `str` в формате RFC3339 или datetime object
        :param route_ids: идентификаторы маршрутов
        :param distributor_ids: идентификаторы прайс-листов
        :param ids: идентификаторы позиций заказов клиентов
        :param order_ids: идентификаторы заказов клиентов
        :param product_ids: идентификаторы карточек товаров через запятую
        :param statuses: список статусов позиций заказов
        :param tag_ids: id тегов
        :param limit: ограничение по кол-ву заказов в выдаче
        :param skip: смещение (по умолчанию 0)
        :param additional_info: доп. информация. Значения `str` или List ["delivery", "unpaidAmount"]
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
        if isinstance(product_ids, int) or isinstance(product_ids, str):
            product_ids = [product_ids]
        if isinstance(route_ids, int) or isinstance(route_ids, str):
            route_ids = [route_ids]
        if isinstance(distributor_ids, int) or isinstance(distributor_ids, str):
            distributor_ids = [distributor_ids]
        if isinstance(ids, int) or isinstance(ids, str):
            ids = [ids]
        if isinstance(order_ids, int) or isinstance(order_ids, str):
            order_ids = [order_ids]
        if isinstance(statuses, str):
            statuses = [statuses]
        if isinstance(tag_ids, list):
            tag_ids = ','.join(map(str, tag_ids))
        if not isinstance(statuses, NoneType):
            statuses = check_fields(statuses, self.FieldsChecker.statuses)
        if not isinstance(additional_info, NoneType):
            additional_info = check_fields(additional_info, self.FieldsChecker.additional_info)
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Positions.GET_LIST, payload)

    async def cancel(self, position_id: Union[str, int], additional_info: Union[List, str] = None):
        """

        :param position_id: идентификатор позиции заказа
        :param additional_info: доп. информация. Значения `str` или List ["delivery", "unpaidAmount"]
        :return:
        """
        if not isinstance(additional_info, NoneType):
            additional_info = check_fields(additional_info, self.FieldsChecker.additional_info)
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Positions.CANCEL, payload, True)

    async def mass_cancel(self, position_ids: Union[List, str, int], additional_info: Union[List, str] = None):
        payload = generate_payload(**locals())
        return await self.request(api.Methods.TsClient.Positions.MASS_CANCEL, payload, True)


class TsClientApi(BaseAbcp):
    def __init__(self, *args):
        super().__init__(*args)
        # If you know how do it other way please commit on https://github.com/bl4ckm45k/aioabcpapi
        self.good_receipts = GoodReceipts(*args)
        self.order_pickings = OrderPickings(*args)
        self.customer_complaints = CustomerComplaints(*args)
        self.orders = Orders(*args)
        self.cart = Cart(*args)
        self.positions = Positions(*args)