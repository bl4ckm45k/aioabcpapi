import logging
from typing import Dict, List, Any

from ..api import _Methods
from ..base import BaseAbcp
from ..exceptions import NotEnoughRights, AbcpAPIError, AbcpParameterRequired, AbcpWrongParameterError
from ..utils.fields_checker import check_limit, process_cp_dates, ensure_list_params, convert_bool_params
from ..utils.payload import generate_payload

logger = logging.getLogger('Cp.Client')


class Search:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @convert_bool_params('use_online_stocks')
    async def brands(self, number: str | int,
                     use_online_stocks: bool | int = 0,
                     locale: str | None = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.B8.D1.81.D0.BA_.D0.B1.D1.80.D0.B5.D0.BD.D0.B4.D0.BE.D0.B2_.D0.BF.D0.BE_.D0.BD.D0.BE.D0.BC.D0.B5.D1.80.D1.83
        Осуществляет поиск по номеру детали и возвращает массив найденных брендов, имеющих деталь с искомым номером.
        Аналог этапа выбора бренда на сайте.
        :param number: Искомый номер детали
        :type number: str or int
        :param use_online_stocks: Флаг "использовать online-склады". Может принимать значения 0 или 1
        :type use_online_stocks: str or int
        :param locale: Локаль. Задается в формате language[_territory], например, ru_RU. По умолчанию используется локаль сайта.
        :type locale: str
        :return:
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Search.BRANDS, payload)

    @convert_bool_params('use_online_stocks', 'disable_online_filtering', 'with_out_analogs')
    async def articles(self,
                       number: str | int,
                       brand: str | int,
                       use_online_stocks: int | bool = 0,
                       disable_online_filtering: int | bool = 0,
                       with_out_analogs: int | bool = 1,
                       profile_id: str | int = None) -> List[Dict[str, Any]]:
        """
        Поиск детали по номеру и бренду.
        
        Осуществляет поиск по номеру детали и бренду. Возвращает массив найденных деталей.
        Так как один и тот же производитель может иметь несколько общепринятых наименований (например, GM и General Motors),
        система постарается это учесть, используя собственную базу синонимов брендов.

        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.B8.D1.81.D0.BA_.D0.B4.D0.B5.D1.82.D0.B0.D0.BB.D0.B8_.D0.BF.D0.BE_.D0.BD.D0.BE.D0.BC.D0.B5.D1.80.D1.83_.D0.B8_.D0.B1.D1.80.D0.B5.D0.BD.D0.B4.D1.83

        :param number: Искомый номер детали
        :type number: :obj:`str` или :obj:`int`
        :param brand: Фильтр по имени производителя
        :type brand: :obj:`str` или :obj:`int`
        :param use_online_stocks: Флаг "использовать online-склады". Может принимать значения 0 или 1 (по умолчанию - 0)
        :type use_online_stocks: :obj:`bool`, :obj:`str` или :obj:`int`
        :param disable_online_filtering: Флаг "отключить фильтры online поставщиков". Может принимать значения 0 или 1 (по умолчанию - 0)
        :type disable_online_filtering: :obj:`bool`, :obj:`str` или :obj:`int`
        :param with_out_analogs: Флаг "исключить поиск по аналогам". По умолчанию - 0.
        :type with_out_analogs: :obj:`bool`, :obj:`str` или :obj:`int`
        :param profile_id: При передаче этого параметра, поисковая выдача api-администратора формируется как для клиента с переданным профилем. Работает только под API-администратором.
        :type profile_id: :obj:`str` или :obj:`int`
        :return: Список найденных деталей
        :rtype: List[Dict[str, Any]]
        :raises NotEnoughRights: Если использован profile_id не API-администратором
        """
        if not self._base.admin and profile_id is not None:
            raise NotEnoughRights('Только API Администор может указывать Профиль пользователя')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Search.ARTICLES, payload)

    @ensure_list_params('search')
    async def batch(self, search: List[Dict] | Dict, profile_id: str | int = None):
        """
        Source https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.B0.D0.BA.D0.B5.D1.82.D0.BD.D1.8B.D0.B9_.D0.B7.D0.B0.D0.BF.D1.80.D0.BE.D1.81_.D0.B1.D0.B5.D0.B7_.D1.83.D1.87.D0.B5.D1.82.D0.B0_.D0.B0.D0.BD.D0.B0.D0.B3.D0.BE.D0.B2
        Осуществляет поиск по номеру производителя и бренду детали. Возвращает массив найденных деталей.
        Внимание! Данная операция не выполняет поиск по online-складам.


        :param search: Набор искомых деталей в формате brand - number. Максимум 100 деталей.
        :type search: dict or list of dicts ({'brand': 'LuK','number': '602000600'})
        :param profile_id: При передаче этого параметра, поисковая выдача api-администратора формируется как для клиента с переданным профилем. Работает только под API-администратором.
        :type profile_id: str or int
        :return:
        """
        if not self._base.admin and profile_id:
            raise NotEnoughRights('Только API Администор может указывать Профиль пользователя')
        payload = generate_payload(exclude=['search'], **locals())
        # It can work with GET and POST, but the documentation specifies POST
        return await self._base.request(_Methods.Client.Search.BATCH, payload, True)

    async def history(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.98.D1.81.D1.82.D0.BE.D1.80.D0.B8.D1.8F_.D0.BF.D0.BE.D0.B8.D1.81.D0.BA.D0.B0
        Возвращает массив последних (не более 50) поисковых запросов текущего пользователя.


        :return: dict
        """
        return await self._base.request(_Methods.Client.Search.HISTORY)

    async def tips(self, number: str | int, locale: str | None):
        """Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.B4.D1.81.D0.BA.D0.B0.D0.B7.D0.BA.D0.B8_.D0.BF.D0.BE_.D0.BF.D0.BE.D0.B8.D1.81.D0.BA.D1.83
        Возвращает по части номера массив подходящих пар бренд - номер


        :param number:Номер (часть номера) детали
        :type number: :obj:`str` or `int`
        :param locale: Локаль. Задается в формате language[_territory], например, ru_RU. По умолчанию используется локаль сайта.
        :type locale: :obj:`str
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Search.TIPS, payload)

    async def advices(self, brand: str | int, number: str | int, limit: int | None = 5):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.B8.D1.81.D0.BA_.D1.81.D0.BE.D0.BF.D1.83.D1.82.D1.81.D1.82.D0.B2.D1.83.D1.8E.D1.89.D0.B8.D1.85_.D1.82.D0.BE.D0.B2.D0.B0.D1.80.D0.BE.D0.B2
        Функция реализует механизм "с этим товаром покупают" на основе статистики покупки комплектов товаров.
        Типичный пример использования функции: покупатель выбрал масляный фильтр - система рекомендует остальные товары из набора для ТО.
        Или, покупатель выбрал левый передний амортизатор, система покажет правый передний.
        Осуществляет поиск сопутствующих товаров по запрашиваемой паре "Бренд-номер".
        Дополнительно можно передать параметр limit (рекомендуется = 5), ограничивающий выдачу рекомендаций.


        :param brand: Имя производителя
        :type brand: :obj:`str | int`
        :param number: Номер детали
        :type number: :obj:`str | int`
        :param limit: необязательный параметр, ограничивающий выдачу
        :type limit :obj:`int`
        :return:
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Search.ADVICES, payload)

    @ensure_list_params('articles')
    async def advices_batch(self, articles: List[Dict] | Dict, limit: int | None = 5):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9C.D0.B5.D1.85.D0.B0.D0.BD.D0.B8.D0.B7.D0.BC_.22.D0.A1_.D1.8D.D1.82.D0.B8.D0.BC_.D1.82.D0.BE.D0.B2.D0.B0.D1.80.D0.BE.D0.BC_.D0.BF.D0.BE.D0.BA.D1.83.D0.BF.D0.B0.D1.8E.D1.82.22
        Функция реализует механизм "с этим товаром покупают" по нескольким товарам.
        Дополнительно можно передать параметр limit (рекомендуется = 5), ограничивающий выдачу рекомендаций.
        Параметры товаров передаются в виде JSON-массива articles из объектов с полями 'brand' и 'number'.


        :param articles:
        :param limit:
        :return:
        """
        payload = generate_payload(exclude=['articles'], **locals())
        return await self._base.request(_Methods.Client.Search.ADVICES_BATCH, payload, post=True, json=True)


class Basket:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get_baskets_list(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD
        Получение списка корзин


        :return: dict
        """
        return await self._base.request(_Methods.Client.Basket.BASKETS_LIST)

    @ensure_list_params('basket_positions')
    async def add(self, basket_positions: List[Dict] | Dict, basket_id: str | int = None) -> Dict[str, Any]:
        """
        Добавление товаров в корзину
        
        Осуществляет подготовку к отправке заказа на товары по номеру производителя, бренду и коду поставки или по коду детали.
        Возвращает статус добавления товара в корзину по каждой позиции.
        
        При добавлении brand-number-itemKey-supplierCode позиции, которая уже была ранее добавлена в корзину,
        значение quantity будет прибавлено к существующему.
        
        Удаление позиции - при добавлении brand-number-itemKey-supplierCode позиции со значением quantity равным 0,
        позиция будет удалена из корзины.

        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.94.D0.BE.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D1.82.D0.BE.D0.B2.D0.B0.D1.80.D0.BE.D0.B2_.D0.B2_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D1.83._.D0.A3.D0.B4.D0.B0.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D1.82.D0.BE.D0.B2.D0.B0.D1.80.D0.B0_.D0.B8.D0.B7_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D1.8B

        :param basket_positions: Набор добавляемых деталей в формате brand-number-itemKey-supplierCode или code
            с указанием добавляемого количества в поле quantity и комментария к позиции в поле comment
        :type basket_positions: :obj:`List[Dict]` или :obj:`Dict`
        :param basket_id: Идентификатор корзины при использовании мультикорзины (необязательный параметр)
        :type basket_id: :obj:`str` или :obj:`int`
        :return: Результат добавления товаров в корзину
        :rtype: Dict[str, Any]
        """
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Client.Basket.BASKET_ADD, payload, True)

    async def clear(self, basket_id: str | int = None):
        """
        Source:https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9E.D1.87.D0.B8.D1.81.D1.82.D0.BA.D0.B0_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D1.8B

        Удаляет все позиции из корзины.


        :param basket_id: Необязательный параметр - идентификатор корзины при использовании мультикорзины
        :type basket_id: :obj:`str | int`
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Basket.BASKET_CLEAR, payload, True)

    async def content(self, basket_id: str | int = None):

        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.82.D0.BE.D0.B2.D0.B0.D1.80.D0.BE.D0.B2_.D0.B2_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D0.B5

        Получение списка товаров в корзине
        Возвращает список позиций, находящихся в корзине.
        Внимание! Если у вас подключена опция "Корзина: разрешать частичное оформление заказа".
        То в ответ веб-сервиса будут попадать только отмеченные позиции.


        :param basket_id: Необязательный параметр - идентификатор корзины при использовании мультикорзины
        :type basket_id: :obj:`str | int`
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Basket.BASKET_CONTENT, payload)

    async def options(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BE.D0.BF.D1.86.D0.B8.D0.B9_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D1.8B

        Получение опций корзины
        Возвращает значение некоторых опций Корзины.

        :return:
        """
        return await self._base.request(_Methods.Client.Basket.BASKET_OPTIONS)

    async def payment_method(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D0.BF.D0.BE.D1.81.D0.BE.D0.B1.D0.BE.D0.B2_.D0.BE.D0.BF.D0.BB.D0.B0.D1.82.D1.8B

        Получение списка способов оплаты
        Возвращает список доступных способов оплаты.
        Идентификатор способа оплаты необходим при отправке заказа (при включенной опции "Корзина: показывать тип оплаты").
        :return:
        """
        return await self._base.request(_Methods.Client.Basket.PAYMENT_METHODS)

    async def shipment_method(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D1.81.D0.BF.D0.BE.D1.81.D0.BE.D0.B1.D0.BE.D0.B2_.D0.B4.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D0.BA.D0.B8

        Получение списка способов доставки

        :return:
        """
        return await self._base.request(_Methods.Client.Basket.SHIPMENT_METHOD)

    async def shipment_offices(self, offices_type: str | None = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BE.D1.84.D0.B8.D1.81.D0.BE.D0.B2_.D1.81.D0.B0.D0.BC.D0.BE.D0.B2.D1.8B.D0.B2.D0.BE.D0.B7.D0.B0

        Получение списка офисов самовывоза
        Возвращает список доступных офисов для самовывоза.
        Идентификатор офиса самовывоза при отправке заказа
        (при включенной опции "Заказы: показывать офисы при выборе самовывоза").


        :param offices_type: Не обязательный параметр:
                            order - (используется по-умолчанию) возвращает офисы используемые для оформления заказа
                            registration - возвращает офисы используемые для регистрации пользователя при включенной опции "Офисы: включить привязку к клиентам"
        :return:
        """
        if isinstance(offices_type, str) and (offices_type != 'order' or offices_type != 'registration'):
            raise AbcpParameterRequired("offices_type может принимать значения 'order' или 'registration'")
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Basket.SHIPMENT_OFFICES, payload)

    async def shipment_address(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B0.D0.B4.D1.80.D0.B5.D1.81.D0.BE.D0.B2_.D0.B4.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D0.BA.D0.B8

        Получение списка адресов доставки
        Возвращает список доступных адресов доставки. Идентификатор адреса доставки необходим при отправке заказа.

        :return:
        """
        return await self._base.request(_Methods.Client.Basket.SHIPMENT_ADDRESS)

    async def shipment_dates(self, min_deadline_time: int, max_deadline_time: int,
                             shipment_address: str | int = None):
        """
        Source:https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B4.D0.B0.D1.82_.D0.BE.D1.82.D0.B3.D1.80.D1.83.D0.B7.D0.BA.D0.B8

        Получение списка дат отгрузки

        Возвращает список доступных дат отгрузки.
        Дата отгрузки необходима при отправке заказа при включенной опции "Корзина: показывать дату отгрузки".


        :param min_deadline_time: Минимальный срок поставки, в часах, среди всех позиций, которые вы собрались отправлять в заказ.
        :param max_deadline_time: Максимальный срок поставки, в часах, среди всех позиций, которые вы собрались отправлять в заказ.
        :param shipment_address: id адреса доставки. Необязательный параметр.
        Необходимо отправлять, если заказ будет оформлен с доставкой.
        Для подготовки доставки офисам может требоваться дополнительное время на сборку.
        При отправке параметра shipmentAddress получаем актуальные даты отгрузки с учетом времени комплектации в настройках офиса.

        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Basket.SHIPMENT_DATES)

    async def add_shipment_address(self, address: str):
        """
        Source:https://www.abcp.ru/wiki/API.ABCP.Client#.D0.94.D0.BE.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B0.D0.B4.D1.80.D0.B5.D1.81.D0.B0_.D0.B4.D0.BE.D1.81.D1.82.D0.B0.D0.B2.D0.BA.D0.B8
        Добавление адреса доставки
        Для текущего покупателя добавляет "адрес доставки" и возвращает его идентификатор используемый в методе Отправка корзины в заказ


        :param address: Обязательный, строка содержащая адрес.
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Basket.SHIPMENT_DATES, payload, True)

    async def set_client_params(self,
                                payment_method_index: int,
                                shipment_address_index: int,
                                shipment_method_index: int = None,
                                shipment_office_index: int = None):
        """
        Устанавливает параметры для метода order.
        Если все индексы переданы верно в методы api.cp.client.order.order_by_basket и api.cp.client.order.order_instant не требуется передавать аргументы:
        'payment_method', 'shipment_address', 'shipment_method', 'shipment_office'.

        :param payment_method_index: Обязательный параметр для любого типа отгрузки. Индекс типа оплаты полученный методом payment_method
        :type payment_method_index: int
        :param shipment_address_index: Обязательный параметр для любого типа отгрузки. Индекс адреса доставки полученный методом shipment_address
        :type shipment_address_index: int
        :param shipment_method_index: Не обязательный параметр, если используется самовывоз. Индекс типа доставки полученный методом payment_method
        :type shipment_method_index: int
        :param shipment_office_index: Не обязательный параметр, если используется доставка. Индекс офиса самовывоза полученый методом shipment_offices
        :type shipment_office_index: int
        :return:
        """
        try:
            if shipment_address_index != 0 and shipment_office_index is not None:
                raise AbcpParameterRequired('Для выбора самовывоза необходимо передать "shipment_address_index=0"')
            payment_method = await self.payment_method()  # 0
            self._base.payment_method = payment_method[payment_method_index]['id']
            logger.info(
                f'Выбран тип оплаты:\nID - {payment_method[payment_method_index]["id"]}\n'
                f'Name - {payment_method[payment_method_index]["name"]}')
            if shipment_method_index is not None and shipment_address_index is not None:
                shipment_address = await self.shipment_address()  # 1
                self._base.shipment_address = shipment_address[shipment_address_index]["id"]
                logger.info(f'Выбран адрес доставки:\nID - {shipment_address[shipment_address_index]["id"]}\n'
                            f'Name - {shipment_address[shipment_address_index]["name"]}')
            if shipment_office_index is not None and shipment_method_index is None:
                shipment_office = await self.shipment_offices()
                self._base.shipment_office = shipment_office[shipment_office_index]["id"]
                logger.info(f'Выбран офис самовывоза:\nID - {shipment_office[shipment_office_index]["id"]}\n'
                            f'Name - {shipment_office[shipment_office_index]["name"]}\n')
            elif shipment_method_index is not None and shipment_office_index is None:
                shipment_method = await self.shipment_method()  # 0
                self._base.shipment_method = shipment_method[shipment_method_index]['id']
                logger.info(f'Выбран тип доставки:\nid - {shipment_method[shipment_method_index]["id"]}\n'
                            f'Name - {shipment_method[shipment_method_index]["name"]}\n')
        except KeyError:
            raise AbcpAPIError('Неверно передан один из индексов')
        except IndexError:
            raise AbcpAPIError('Неверно передан один из индексов')


class Orders:
    def __init__(self, base: BaseAbcp):
        self._base = base

    @process_cp_dates('shipment_date')
    async def order_by_basket(self,
                              payment_method: str = None,
                              shipment_method: str = None,
                              shipment_address: str = None,
                              shipment_office: str = None,
                              shipment_date: str = None,
                              comment: str = None,
                              basket_id: str = None,
                              whole_order_only: int = None,
                              position_ids: List = None,
                              client_order_number: str | int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9E.D1.82.D0.BF.D1.80.D0.B0.D0.B2.D0.BA.D0.B0_.D0.BA.D0.BE.D1.80.D0.B7.D0.B8.D0.BD.D1.8B_.D0.B2_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7
        Отправка корзины в заказ
        Осуществляет отправку позиций, содержащихся в корзине, в заказ.
        Возвращает статус операции, а так же список созданных заказов со списками позиций в каждом из них.
        Внимание!
        При отправке заказа могут возникнуть ошибки, при этом, часть позиций могут отправиться.
        Следовательно, независимо от статуса выполнения операции, необходимо проверять узел orders на наличие сформированных заказов.


        :param payment_method: 	Идентификатор способа оплаты.
        :param shipment_method: Идентификатор способа доставки.
        :param shipment_address: Идентификатор адреса доставки.
        :param shipment_office: Идентификатор офиса самовывоза
        :param shipment_date: Дата отгрузки.
        :param comment: Комментарий к заказу.
        :param basket_id: Необязательный параметр - идентификатор корзины при использовании мультикорзины
        :param whole_order_only: Признак - оформить заказ целиком. Принимаемые значения - 0/1. По умолчанию - 0.
        :param position_ids: Необязательный параметр - массив с номерами позиций заказа. Номера возвращает метод basket_content
        :param client_order_number: Необязательный параметр - номер заказа в системе учета клиента
        :return:
        """
        if payment_method is None:
            payment_method = self._base.payment_method
        if shipment_method is None:
            shipment_method = self._base.shipment_method
        if shipment_address is None:
            shipment_address = self._base.shipment_address
        if shipment_office is None:
            shipment_office = self._base.shipment_office
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Basket.BASKET_ORDER, payload, True)

    async def order_instant(self, positions: List[Dict] | Dict,
                            payment_method: str = None, shipment_method: str = None,
                            shipment_address: str = None, shipment_office: str = None, shipment_date: str = None,
                            comment: str = None, basket_id: str = None, whole_order_only: int = 0,
                            client_order_number: str = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9C.D0.BE.D0.BC.D0.B5.D0.BD.D1.82.D0.B0.D0.BB.D1.8C.D0.BD.D1.8B.D0.B9_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7
        Объединяет в себе операции basket/add и basket/order то есть, добавляет переданный в параметрах список товаров в корзину и сразу же отправляет их в заказ.
        У данной операции есть важная особенность - она не учитывает позиции, которые уже лежат в корзине,
        в заказ они не попадут и останутся в корзине пользователя. Использование данной операции оптимально при автоматическом перезаказе у клиентов платформы ABCP.


        :param positions: Набор добавляемых деталей в формате {'brand': luk, 'number': '602000600', 'itemKey': 'Xqgs...', 'supplierCode': '1234', 'quantity': 1, 'comment': 'Hello, part of world'}
        :param payment_method: 	Идентификатор способа оплаты.
        :type payment_method: str
        :param shipment_method: Идентификатор способа доставки.
        :type shipment_method: str
        :param shipment_address: Идентификатор адреса доставки.
        :type shipment_address: str
        :param shipment_office: Идентификатор офиса самовывоза
        :type shipment_office: str
        :param shipment_date: Дата отгрузки.
        :type shipment_date: str
        :param comment: Комментарий к заказу.
        :type comment: str
        :param basket_id: Необязательный параметр - идентификатор корзины при использовании мультикорзины
        :type basket_id: str
        :param whole_order_only: Признак - оформить заказ целиком. Принимаемые значения - 0/1. По умолчанию - 0.
        :type whole_order_only: int
        :param client_order_number: Необязательный параметр - номер заказа в системе учета клиента
        :type client_order_number: str
        :return:
        """
        if isinstance(positions, dict):
            basket_positions = [positions]
        else:
            basket_positions = positions
        del positions
        if payment_method is None:
            payment_method = self._base.payment_method
        if shipment_method is None:
            shipment_method = self._base.shipment_method
        if shipment_address is None:
            shipment_address = self._base.shipment_address
        if shipment_office is None:
            shipment_office = self._base.shipment_office
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Orders.ORDERS_INSTANT, payload, True)

    @ensure_list_params('orders')
    async def orders_list(self, orders: List | str | int):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B9_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.BE.D0.B2_.D1.81.D0.BE_.D1.81.D1.82.D0.B0.D1.82.D1.83.D1.81.D0.B0.D0.BC.D0.B8


        :param orders: Список номеров заказа или один номер заказа
        :type orders: :obj:`list` or :obj:`str`
        :return:
        """

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Orders.GET_ORDERS_LIST, payload)

    @check_limit
    async def get_orders(self, format: str = None, skip: int | None = None, limit: int | None = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B7.D0.B0.D0.BA.D0.B0.D0.B7.D0.BE.D0.B2
        Получение списка заказов
        Осуществляет получение списка всех заказов клиента по страницам.
        Сортировка по номеру заказа по убыванию, т.е. сначала передаются самые новые заказы.

        :param format: (необязательный) - формат вывода результата. По умолчанию отображается информация только по заказам. При значении p - к заказам добавляется информация по всем позициям.
        :param skip: (необязательный) - кол-во заказов, которые нужно пропустить. По умолчанию - 0.
        :param limit: 	(необязательный) - кол-во заказов, которые нужно отобразить за один раз. Допускается любое значение от 1 до 1000. По умолчанию - 100.
        :return:
        """
        if isinstance(format, str) and format != 'p':
            raise AbcpWrongParameterError("format", format, 'может принимать только значение "p"')

        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Orders.GET_ORDERS, payload)

    async def cancel_position(self, position_id: int):
        """
        Source:https://www.abcp.ru/wiki/API.ABCP.Client#.D0.97.D0.B0.D0.BF.D1.80.D0.BE.D1.81_.D0.BD.D0.B0_.D0.BE.D1.82.D0.BC.D0.B5.D0.BD.D1.83_.D0.BF.D0.BE.D0.B7.D0.B8.D1.86.D0.B8.D0.B8
        Запрос на отмену позиции
        Выставляет позиции признак "Запрос на отмену"


        :param position_id: Идентификатор позиции заказа
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Orders.CANCEL_POSITION, payload, True)


class User:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def register(self,
                       market_type: str | int,
                       name: str, second_name: str, surname: str,
                       password: str, mobile: str,
                       office: str | int, email: str,
                       icq: str | int = None, skype: str = None,
                       region_id: str | int = None,
                       business: str | int = None,
                       organization_name: str = None,
                       organization_form: str = None,
                       organization_official_name: str = None,
                       inn: str | int = None,
                       kpp: str | int = None,
                       ogrn: str | int = None,
                       organization_official_address: str | int = None,
                       bank_name: str = None,
                       bik: str | int = None,
                       correspondent_account: str | int = None,
                       organization_account: str | int = None,
                       delivery_address: str = None,
                       comment: str = None,
                       send_registration_email: str | int = None,
                       member_of_club: str = None,
                       birth_date: str = None,
                       filial_id: str | int = None,
                       profile_id: str | int = None,
                       ):

        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.A0.D0.B5.D0.B3.D0.B8.D1.81.D1.82.D1.80.D0.B0.D1.86.D0.B8.D1.8F_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.BB.D1.8F
        Принимает параметры для регистрации пользователя.
        Осуществляет регистрацию нового пользователя в системе.
        Возвращает статус выполнения операции регистрации, учетные данные нового пользователя, а так же сообщение об ошибке в случае возникновения таковой.
        Регистрация через API запрещена при использовании модуля франчайзи, если выключен флаг "Головная компания (ГК) участвует в продажах".

        :param market_type: Тип регистрации: 1. Розница 2. Опт
        :param name: Имя
        :param second_name: Отчество
        :param surname: Фамилия
        :param password: Пароль
        :param mobile: Номер мобильного телефона
        :param office: Идентификатор офиса
        :param email: Почта
        :param profile_id: Идентификатор профиля (Только для API администратора)
        :param icq: ICQ UIN
        :param skype: Skype
        :param region_id: Код региона
        :param business: Тип организации от 1 до 3. Автосервис, Автомагазин, Собственный автопарк
        :param organization_name: Наименование организации
        :param organization_form: Правовая форма организации. Варианты: ООО, ОАО, ЗАО, ТОО, АО, ЧП, ПБОЮЛ
        :param organization_official_name: Наименование по регистрации (без правовой формы юр. лица)
        :param inn: ИНН
        :param kpp: КПП
        :param ogrn: ОГРН
        :param organization_official_address: Юридический адрес организации
        :param bank_name: Наименование банка
        :param bik: БИК
        :param correspondent_account: Корреспондентский счет банка
        :param organization_account: Расчетный счет организации
        :param delivery_address: Адрес доставки
        :param comment: Комментарий
        :param send_registration_email: Необязательный, по-умолчанию - 0. 1 - отправлять клиенту, менеджеру письмо о регистрации 0 - не отправлять письмо
        :param member_of_club: Название автоклуба
        :param birth_date: Дата рождения, формат YYYY-MM-DD
        :param filial_id: Код филиала (если имеются)
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.User.REGISTER, payload, True)

    async def activate(self, user_code: int, activation_code: str | int):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.90.D0.BA.D1.82.D0.B8.D0.B2.D0.B0.D1.86.D0.B8.D1.8F_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.BB.D1.8F


        :param user_code: Внутренний код пользователя
        :param activation_code: Код активации
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.User.ACTIVATION, payload, True)

    async def user_info(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B4.D0.B0.D0.BD.D0.BD.D1.8B.D1.85_.D0.BF.D0.BE.D0.BB.D1.8C.D0.B7.D0.BE.D0.B2.D0.B0.D1.82.D0.B5.D0.BB.D1.8F_.28.D0.B0.D0.B2.D1.82.D0.BE.D1.80.D0.B8.D0.B7.D0.B0.D1.86.D0.B8.D1.8F.29
        Получение данных пользователя (авторизация)
        Возвращает данные пользователя по логину и паролю.

        :return:
        """
        return await self._base.request(_Methods.Client.User.USER_INFO)

    async def restore(self, email_or_mobile: str = None, password_new: str = None, code: str = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.92.D0.BE.D1.81.D1.81.D1.82.D0.B0.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.BF.D0.B0.D1.80.D0.BE.D0.BB.D1.8F
        Операция восстановление пароля пользователя.
        Восстановление пароля состоит из двух этапов:

        1. Запрос восстановления пароля с указанием номера телефона или email.
        В результате успешного завершения будет отправлено стандартное письмо со ссылкой восстановления пароля на указанный email или код в SMS на указанный номер телефона.
        2. Сохранение нового пароля с указанием кода подтверждения из SMS.
        !!!Внимание!!!
        Данный этап актуален только для восстановления по номеру телефона,
        так как в случае с email, в письме придет ссылка на форму восстановления пароля на сайте, и второй этап будет выполнен в ней.
        :param email_or_mobile:
        :param password_new:
        :param code:
        :return:
        """
        if email_or_mobile is not None and any(x is not None for x in [password_new, code]):
            raise AbcpAPIError('E-mail или мобильный используется только для первого этапа восстановления.'
                               'А password_new и code для второго')
        if email_or_mobile is None and any(x is None for x in [password_new, code]):
            raise AbcpAPIError('Для второго этапа должны быть указаны password_new и code ')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.User.USER_RESTORE, payload, True)


class Garage:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def get_list(self, user_id: str | int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.B0.D0.B2.D1.82.D0.BE.D0.BC.D0.BE.D0.B1.D0.B8.D0.BB.D0.B5.D0.B9_.D0.B2_.D0.B3.D0.B0.D1.80.D0.B0.D0.B6.D0.B5
        Получение списка автомобилей в гараже


        :param user_id: Указывается API администратором
        :return:
        """
        if user_id and not self._base.admin:
            raise AbcpAPIError('Параметр "user_id" может быть передан только API администратором')
        return await self._base.request(_Methods.Client.Garage.USER_GARAGE)

    async def get_car(self, car_id: int, user_id: str | int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B8.D0.BD.D1.84.D0.BE.D1.80.D0.BC.D0.B0.D1.86.D0.B8.D0.B8_.D0.BE.D0.B1_.D0.B0.D0.B2.D1.82.D0.BE.D0.BC.D0.BE.D0.B1.D0.B8.D0.BB.D0.B5_.D0.B2_.D0.B3.D0.B0.D1.80.D0.B0.D0.B6.D0.B5
        Получение информации об автомобиле в гараже

        Возвращает данные по одному автомобилю гаража текущего пользователя


        :param user_id: Указывается API администратором
        :param car_id: Идентификатор автомобиля в гараже
        :return:
        """
        if user_id and not self._base.admin:
            raise AbcpAPIError('Параметр "user_id" может быть передан только API администратором')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Garage.GARAGE_CAR, payload)

    async def add(self, name: str,
                  comment: str = None, year: str = None, vin: str = None,
                  frame: str = None,
                  mileage: str = None,
                  manufacturer_id: str | int = None,
                  model_id: str | int = None,
                  modification_id: str | int = None,
                  vehicle_reg_plate: str = None,
                  user_id: str | int = None):

        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.94.D0.BE.D0.B0.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B0.D0.B2.D1.82.D0.BE.D0.BC.D0.BE.D0.B1.D0.B8.D0.BB.D1.8F_.D0.B2_.D0.B3.D0.B0.D1.80.D0.B0.D0.B6



        :param name: Название автомобиля (пользовательское)
        :param comment: Комментарий (пользовательский)
        :param year: Год выпуска автомобиля
        :param vin: VIN-код автомобиля
        :param frame: Номер кузова автомобиля
        :param mileage: Пробег автомобиля
        :param manufacturer_id: Идентификатор марки автомобиля
        :param model_id: Идентификатор модели автомобиля
        :param modification_id: Идентификатор модификации автомобиля
        :param vehicle_reg_plate: Государственный номер автомобиля
        :param user_id: Указывается API администратором
        :return:
        """
        if user_id and not self._base.admin:
            raise AbcpAPIError('Параметр "user_id" может быть передан только API администратором')
        payload = generate_payload(**locals())

        return await self._base.request(_Methods.Client.Garage.GARAGE_ADD, payload, True)

    async def update(self, car_id: int, name: str = None,
                     comment: str = None, year: str = None, vin: str = None,
                     frame: str = None,
                     mileage: str = None,
                     manufacturer_id: str | int = None,
                     model_id: str | int = None,
                     modification_id: str | int = None,
                     vehicle_reg_plate: str = None,
                     user_id: str | int = None):

        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9E.D0.B1.D0.BD.D0.BE.D0.B2.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B0.D0.B2.D1.82.D0.BE.D0.BC.D0.BE.D0.B1.D0.B8.D0.BB.D1.8F_.D0.B2_.D0.B3.D0.B0.D1.80.D0.B0.D0.B6.D0.B5
        Обновление машины в гараже.
        Изменяет автомобиль в гараже.
        Обязательным свойством автомобиля является только carId, то есть, можно передавать только те параметры, которые необходимо изменить.
        Не переданные свойства изменены не будут.

        :param car_id: Идентификатор автомобиля
        :param name: Название автомобиля (пользовательское)
        :param comment: Комментарий (пользовательский)
        :param year: Год выпуска автомобиля
        :param vin: VIN-код автомобиля
        :param frame: Номер кузова автомобиля
        :param mileage: Пробег автомобиля
        :param manufacturer_id: Идентификатор марки автомобиля
        :param model_id: Идентификатор модели автомобиля
        :param modification_id: Идентификатор модификации автомобиля
        :param vehicle_reg_plate: Государственный номер автомобиля
        :param user_id: Указывается API администратором
        :return:
        """
        if user_id and not self._base.admin:
            raise AbcpAPIError('Параметр "user_id" может быть передан только API администратором')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Garage.GARAGE_UPDATE, payload, True)

    async def delete(self, car_id: int, user_id: str | int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.A3.D0.B4.D0.B0.D0.BB.D0.B5.D0.BD.D0.B8.D0.B5_.D0.B0.D0.B2.D1.82.D0.BE.D0.BC.D0.BE.D0.B1.D0.B8.D0.BB.D1.8F_.D0.B8.D0.B7_.D0.B3.D0.B0.D1.80.D0.B0.D0.B6.D0.B0
        Удаление автомобиля из гаража


        :param car_id:
        :param user_id: Указывается API администратором
        :return:
        """
        if user_id and not self._base.admin:
            raise AbcpAPIError('Параметр "user_id" может быть передан только API администратором')
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Garage.GARAGE_DELETE, payload, True)


class CarTree:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def years(self, manufacturer_id: str | int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.94.D0.B5.D1.80.D0.B5.D0.B2.D0.BE_.D0.B0.D0.B2.D1.82.D0.BE.D0.BC.D0.BE.D0.B1.D0.B8.D0.BB.D0.B5.D0.B9
        Получение списка годов дерева автомобилей
        Возвращает список доступных годов для дерева автомобилей


        :param manufacturer_id: Идентификатор марки для фильтрации. Необязательное.
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.CarTree.CAR_TREE_YEARS, payload)

    async def manufacturers(self, year: int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BC.D0.B0.D1.80.D0.BE.D0.BA_.D0.B4.D0.B5.D1.80.D0.B5.D0.B2.D0.B0_.D0.B0.D0.B2.D1.82.D0.BE.D0.BC.D0.BE.D0.B1.D0.B8.D0.BB.D0.B5.D0.B9
        Получение списка марок дерева автомобилей
        Возвращает список доступных марок для дерева автомобилей


        :param year: Год для фильтрации марок. Необязательное.
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.CarTree.CAR_TREE_MANUFACTURERS, payload)

    async def models(self, manufacturer_id: str | int = None, year: str | int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BC.D0.BE.D0.B4.D0.B5.D0.BB.D0.B5.D0.B9_.D0.B4.D0.B5.D1.80.D0.B5.D0.B2.D0.B0_.D0.B0.D0.B2.D1.82.D0.BE.D0.BC.D0.BE.D0.B1.D0.B8.D0.BB.D0.B5.D0.B9


        :param manufacturer_id: Идентификатор марки
        :param year: Год для фильтрации моделей. Необязательное.
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.CarTree.CAR_TREE_MODELS, payload)

    async def modifications(self, manufacturer_id: str | int = None, model_id: str | int = None,
                            year: str | int = None):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BC.D0.BE.D0.B4.D0.B8.D1.84.D0.B8.D0.BA.D0.B0.D1.86.D0.B8.D0.B9_.D0.B4.D0.B5.D1.80.D0.B5.D0.B2.D0.B0_.D0.B0.D0.B2.D1.82.D0.BE.D0.BC.D0.BE.D0.B1.D0.B8.D0.BB.D0.B5.D0.B9


        :param manufacturer_id: Идентификатор марки
        :param model_id: Идентификатор модели
        :param year: Год для фильтрации моделей. Необязательное.
        :return:
        """
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.CarTree.CAR_TREE_MODIFICATIONS, payload)


class Form:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def fields(self, name: str, locale: str = None):
        """
        Source:  https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D0.B8.D1.81.D0.BA.D0.B0_.D0.BF.D0.BE.D0.BB.D0.B5.D0.B9_.D1.84.D0.BE.D1.80.D0.BC.D1.8B
        Получение списка полей формы

        Возвращает список полей формы и все параметры в соответствии с установленными настройками в панели управления на странице Внешний вид и контент / Формы.
        На текущий момент доступны только формы регистрации, реализованные в API-методе user/new.

        :param name: Имя формы. Возможные значения: registration_wholesale - опт; registration_retail - розница
        :param locale: 	Локаль формы (по умолчанию, ru_RU)
        :return:
        """
        if name not in ['registration_wholesale', 'registration_retail']:
            raise AbcpWrongParameterError("name",
                                          name,
                                          "must be one of: 'registration_wholesale', 'registration_retail'")
        payload = generate_payload(**locals())
        return await self._base.request(_Methods.Client.Form.FIELDS, payload)


class Articles:
    def __init__(self, base: BaseAbcp):
        self._base = base

    async def brands(self):
        """
        Source: https://www.abcp.ru/wiki/API.ABCP.Client#.D0.9F.D0.BE.D0.BB.D1.83.D1.87.D0.B5.D0.BD.D0.B8.D0.B5_.D1.81.D0.BF.D1.80.D0.B0.D0.B2.D0.BE.D1.87.D0.BD.D0.B8.D0.BA.D0.B0_.D0.B1.D1.80.D0.B5.D0.BD.D0.B4.D0.BE.D0.B2
        Получение справочника брендов
        Возвращает список всех брендов зарегистрированных в системе с их синонимами.


        :return:
        """
        return await self._base.request(_Methods.Client.Articles.BRANDS)

    @ensure_list_params('source')
    async def info(self, brand: str | int, number: str | int,
                   format: str, source: List | str,
                   cross_image: int = None,
                   with_original: str = None,
                   locale: str = None):
        if not self._base.admin:
            raise AbcpAPIError('Операция доступна только администратору API')
        if isinstance(format, str) and format not in 'bnpchmti':
            raise AbcpWrongParameterError("format",
                                          format,
                                          'может содержать только символы: b, n, p, c, h, m, t, i')

        if isinstance(source, list) and not all(x in ['standard', 'common', 'common_cat'] for x in source):
            raise AbcpWrongParameterError("source",
                                          source,
                                          'может содержать следующие флаги: standard, common, common_cat')

        payload = generate_payload(exclude=['cross_image', 'with_original'], **locals())
        return await self._base.request(_Methods.Client.Articles.INFO, payload)


class ClientApi:
    """
    API для клиента ABCP
    
    Предоставляет доступ ко всем методам API для клиента.
    """

    def __init__(self, base: BaseAbcp):
        """
        Инициализация API клиента
        
        :param base: Объект с базовой конфигурацией API
        :type base: BaseAbcp
        """
        self._base = base
        self._search = None
        self._basket = None
        self._orders = None
        self._user = None
        self._garage = None
        self._car_tree = None
        self._form = None
        self._articles = None

    @property
    def search(self) -> Search:
        """
        Доступ к методам поиска
        
        :return: Объект с методами поиска
        :rtype: Search
        """
        if self._search is None:
            self._search = Search(self._base)
        return self._search

    @property
    def basket(self) -> Basket:
        """
        Доступ к методам работы с корзиной
        
        :return: Объект с методами корзины
        :rtype: Basket
        """
        if self._basket is None:
            self._basket = Basket(self._base)
        return self._basket

    @property
    def orders(self) -> Orders:
        """
        Доступ к методам работы с заказами
        
        :return: Объект с методами заказов
        :rtype: Orders
        """
        if self._orders is None:
            self._orders = Orders(self._base)
        return self._orders

    @property
    def user(self) -> User:
        """
        Доступ к методам работы с пользователем
        
        :return: Объект с методами пользователя
        :rtype: User
        """
        if self._user is None:
            self._user = User(self._base)
        return self._user

    @property
    def garage(self) -> Garage:
        """
        Доступ к методам работы с гаражом
        
        :return: Объект с методами гаража
        :rtype: Garage
        """
        if self._garage is None:
            self._garage = Garage(self._base)
        return self._garage

    @property
    def car_tree(self) -> CarTree:
        """
        Доступ к методам работы с деревом автомобилей
        
        :return: Объект с методами дерева автомобилей
        :rtype: CarTree
        """
        if self._car_tree is None:
            self._car_tree = CarTree(self._base)
        return self._car_tree

    @property
    def form(self) -> Form:
        """
        Доступ к методам работы с формами
        
        :return: Объект с методами форм
        :rtype: Form
        """
        if self._form is None:
            self._form = Form(self._base)
        return self._form

    @property
    def articles(self) -> Articles:
        """
        Доступ к методам работы с артикулами
        
        :return: Объект с методами артикулов
        :rtype: Articles
        """
        if self._articles is None:
            self._articles = Articles(self._base)
        return self._articles
