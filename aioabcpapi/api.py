import re
from typing import Dict, Union

import aiohttp
import logging
from .exceptions import UnsupportedHost, PasswordType, UnsupportedLogin, NotEnoughRights, NetworkError, \
    AbcpAPIError, TeaPot
from http import HTTPStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


def check_data(host: str, login: str, password: str):
    regex_md = re.match(r"([a-f\d]{32})", password)
    if regex_md:
        host_id = host.split('.')[0][2:]
        if host_id.isdigit() and len(host_id) < 6 and host[0:2] == 'id':
            if login[0:6] == 'api@id' and login[6:] == host_id:
                return True
            else:
                if login.isdigit() and 4 < len(login) < 14:
                    return False
                elif '@' in login:
                    email = re.match('^[\w.]+@([\w-]+\.)+[\w-]{2,6}$', login, flags=re.IGNORECASE)
                    if email:
                        return False
                    else:
                        raise UnsupportedLogin('Недопустимый логин')
                else:
                    raise UnsupportedLogin('Недопустимый логин')
        else:
            raise UnsupportedHost(f'Имя хоста {host} не поддерживается\n'
                                  f'Допустимые имена id200.public.api.abcp.ru')
    else:
        raise PasswordType(f'Допускаются пароли только в md5 hash')


def check_result(method_name: str, content_type: str, status_code: int, body):
    """
    Checks whether `result` is a valid API response.
    A result is considered invalid if:
    - The server returned an HTTP response code other than 200
    - The content of the result is invalid JSON.
    - The method call was unsuccessful (The JSON 'ok' field equals False)

    :param method_name: The name of the method called
    :param status_code: status code
    :param content_type: content type of result
    :param body: result body
    :return: The result parsed to a JSON dictionary
    :raises ApiException: if one of the above listed cases is applicable
    """
    logger.debug('Response for %s: [%d] "%r"', method_name, status_code, body)

    if content_type != 'application/json':
        raise NetworkError(f"Invalid response with content type {content_type}: \"{body}\"")

    if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED:
        return body
    elif status_code == HTTPStatus.BAD_REQUEST:
        raise AbcpAPIError(f"{body['errorMessage']} {body['errorCode']} [{status_code}]")
    elif status_code == HTTPStatus.NOT_FOUND:
        raise AbcpAPIError(f"{body['errorMessage']} {body['errorCode']} [{status_code}]")
    elif status_code == HTTPStatus.CONFLICT:
        raise AbcpAPIError(f"{body} [{status_code}]")
    elif status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
        raise AbcpAPIError(f"{body} [{status_code}]")
    elif status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        raise AbcpAPIError(f"{body} [{status_code}]")
    elif status_code == HTTPStatus.IM_A_TEAPOT:
        raise TeaPot("RFC 2324, секция 2.3.2: 418 I'm a teapot")

    raise AbcpAPIError(f"{body} [{status_code}]")


async def make_request_json(session, url, method, data: Dict, headers, **kwargs):
    try:
        async with session.post(url, json=data, headers=headers, **kwargs) as response:
            try:
                body = await response.json()
            except:
                body = response.text
            return check_result(method, response.content_type, response.status, body)
    except aiohttp.ClientError as e:
        raise NetworkError(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")


async def make_request(session, host, admin, method,
                       data: Union[Dict, aiohttp.FormData()], post,
                       **kwargs):
    logger.debug('Make request: "%s" with data: "%r"', method, data)

    if not admin and method[0:2] == 'cp':
        raise NotEnoughRights('Недостаточно прав для использования API администратора')
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    url = f'https://{host}/{method}'
    if method == Methods.Admin.UPLOAD_PRICE:
        headers = None
    elif method == Methods.Client.ADVICES_BATCH:
        headers['Content-Type'] = 'application/json'
        return await make_request_json(session, url, method, data, headers)
    try:
        if post:
            async with session.post(url, data=data, headers=headers, **kwargs) as response:
                try:
                    body = await response.json()
                except:
                    body = response.text
                return check_result(method, response.content_type, response.status, body)
        else:
            async with session.get(url, params=data, **kwargs) as response:
                try:
                    body = await response.json()
                except:
                    body = response.text
                return check_result(method, response.content_type, response.status, body)
    except aiohttp.ClientError as e:
        raise NetworkError(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")


class Methods:
    class Admin:
        GET_ORDERS_LIST = 'cp/orders'  # Получение списка заказов (get)
        GET_ORDER = 'cp/order'  # Получение информации о заказе (get)
        STATUS_HISTORY = 'cp/order/statusHistory'  # Получение истории изменений статуса позиции заказа (get)
        SAVE_ORDER = 'cp/order'  # Сохранение заказа (post)

        # Supplier order

        GET_PARAMS_FOR_ONLINE_ORDER = 'cp/orders/online'  # Получение параметров для отправки online-заказа поставщику (get)
        SEND_ONLINE_ORDER = 'cp/orders/online'  # Отправка online-заказа поставщику (post)

        # Finance
        UPDATE_BALANCE = 'cp/finance/userBalance'  # Обновление баланса клиента (post)
        UPDATE_CREDIT_LIMIT = 'cp/finance/creditLimit'  # Обновление лимита кредита клиента (post)
        UPDATE_FINANCE_INFO = 'cp/finance/userInfo'  # Обновление финансовой информации клиента (post)
        GET_PAYMENTS = 'cp/finance/payments'  # Получение информации об оплатах из финмодуля (get)
        GET_PAYMENTS_LINKS = 'cp/finance/paymentOrderLinks'  # Получение информации о привязках платежей из модуля Финансы (get)
        GET_PAYMENTS_ONLINE = 'cp/onlinePayments'  # Получение списка online платежей (get)
        ADD_PAYMENTS = 'cp/finance/payments'  # Добавление оплат (post)
        DELETE_PAYMENT_LINK = 'cp/finance/deleteLinkPayments'  # Удаление привязки оплаты (post)
        LINK_EXISTING_PLAYMENT = 'cp/finance/paymentOrderLink'  # Операция привязки по ранее добавленному платежу (post)
        REFUND_PAYMENT = 'cp/finance/paymentRefund'  # Операция возврата платежа (post)
        GET_RECEIPTS = 'komtet/getChecks'  # Получение списка чеков (get)

        # Users
        GET_USERS_LIST = 'cp/users'  # Получение списка пользователей (get)
        CREATE_USER = 'cp/user/new'  # Создание пользователя (post)
        GET_PROFILES = 'cp/users/profiles'  # Получение списка профилей (get)
        EDIT_PROFILE = 'cp/users/profile'  # Обновление профиля (post)

        EDIT_USER = 'cp/user'  # Обновление данных пользователя (post)

        GET_USER_SHIPMENT_ADDRESS = 'cp/user/shipmentAddresses'  # Получение списка адресов доставки (get)

        # Staff

        GET_STAFF = 'cp/managers'  # Получение списка сотрудников (get)

        # Statuses

        GET_STATUSES = 'cp/statuses'  # Получение списка статусов (get)

        # Brand directory

        GET_BRANDS = 'cp/artiles/brands'  # Получение справочника брендов (get)

        # Suppliers

        GET_DISTRIBUTORS_LIST = 'cp/distributors'  # Получение списка поставщиков (get)
        EDIT_DISTRIBUTORS_STATUS = 'cp/distributor/status'  # Изменение статуса поставщика (post)
        UPLOAD_PRICE = 'cp/distributor/pricelistUpdate'  # Загрузка прайс-листа поставщика (post)

        GET_SUPPLIER_ROUTES = 'cp/routes'  # Получение списка маршрутов поставщика (get)
        UPDATE_ROUTE = 'cp/route'  # Обновление данных маршрута поставщика (post)
        UPDATE_ROUTE_STATUS = 'cp/routes/status'  # Изменение статуса маршрута поставщика
        DELETE_ROUTE = 'cp/route/delete'  # Удаление маршрута поставщика (post)
        EDIT_SUPPLIER_STATUS_FOR_OFFICE = 'cp/offices'  # Подключение поставщиков к офису (post)
        GET_OFFICE_SUPPLIERS = 'cp/offices'  # Получение поставщиков офиса (get)

        # Garage

        GET_USERS_CARS = 'cp/garage'  # Получение списка обновлённых автомобилей в гараже

        # Payments settings

        GET_PAYMENTS_SETTINGS = 'cp/payments/getPaymentMethodSettings'  # Получение списка настроек платёжных систем

    class Client:
        # SARCH METHODS

        SEARCH_BRANDS = 'search/brands'
        SEARCH_ARTICLES = 'search/articles'
        SEARCH_BATCH = 'search/batch'
        SEARCH_HISTORY = 'search/history'
        SEARCH_TIPS = 'search/tips'
        ADVICES = 'advices'
        ADVICES_BATCH = 'advices/batch'

        # BASKET METHODS

        BASKETS_LIST = 'basket/multibasket'
        BASKET_ADD = 'basket/add'
        BASKET_CLEAR = 'basket/clear'
        BASKET_CONTENT = 'basket/content'
        BASKET_OPTIONS = 'basket/options'
        PAYMENT_METHODS = 'basket/paymentMethods'
        SHIPMENT_METHOD = 'basket/shipmentMethods'
        SHIPMENT_OFFICES = 'basket/shipmentOffices'
        SHIPMENT_ADDRESS = 'basket/shipmentAddresses'
        SHIPMENT_DATES = 'basket/shipmentDates'
        BASKET_ORDER = 'basket/order'

        ORDERS_INSTANT = 'orders/instant'
        GET_ORDERS_LIST = 'orders/list'
        GET_ORDERS = 'orders'
        CANCEL_POSITION = 'orders/cancelPosition'

        REGISTER = 'user/new'
        ACTIVATION = 'user/activation'
        USER_INFO = 'user/info'
        USER_RESTORE = 'user/restore'

        USER_GARAGE = 'user/garage'
        GARAGE_CAR = 'user/garage/car'
        GARAGE_ADD = 'user/garage/add'
        GARAGE_UPDATE = 'user/garage/update'
        GARAGE_DELETE = 'user/garage/delete'

        CARTREE_YEARS = 'cartree/years'
        CARTREE_MANUFACTURERS = 'cartree/manufacturers'
        CARTREE_MODELS = 'cartree/models'
        CARTREE_MODIFICATIONS = 'cartree/modifications'

        FORM_FIELDS = 'form/fields'
        ARTICLES_BRANDS = 'articles/brands'
        ARTICLES_INFO = 'articles/info'