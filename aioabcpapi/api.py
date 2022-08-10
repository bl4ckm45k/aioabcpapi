import logging
import re
from http import HTTPStatus
from typing import Dict, Union

import aiohttp

from .exceptions import UnsupportedHost, PasswordType, UnsupportedLogin, NotEnoughRights, NetworkError, \
    AbcpAPIError, TeaPot, AbcpNotFoundError

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
        if any(method_name == x for x in SEARCH_METHODS):
            raise AbcpNotFoundError(f"{body['errorMessage']} {body['errorCode']} [{status_code}]")
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
                       data: Union[Dict, aiohttp.FormData], post,
                       **kwargs):
    logger.debug('Make request: "%s" with data: "%r"', method, data)

    if not admin and method[0:2] == 'cp':
        raise NotEnoughRights('Недостаточно прав для использования API администратора')
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    url = f'https://{host}/{method}'
    if method == Methods.Admin.Distributors.UPLOAD_PRICE:
        headers = None
    elif method == Methods.Client.Search.ADVICES_BATCH:
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
        class Orders:
            GET_ORDERS_LIST = 'cp/orders'
            GET_ORDER = 'cp/order'
            STATUS_HISTORY = 'cp/order/statusHistory'
            SAVE_ORDER = 'cp/order'

            # Supplier order

            ONLINE_ORDER = 'cp/orders/online'

        class Finance:
            UPDATE_BALANCE = 'cp/finance/userBalance'
            UPDATE_CREDIT_LIMIT = 'cp/finance/creditLimit'
            UPDATE_FINANCE_INFO = 'cp/finance/userInfo'
            GET_PAYMENTS = 'cp/finance/payments'
            GET_PAYMENTS_LINKS = 'cp/finance/paymentOrderLinks'
            GET_PAYMENTS_ONLINE = 'cp/onlinePayments'
            ADD_PAYMENTS = 'cp/finance/payments'
            DELETE_PAYMENT_LINK = 'cp/finance/deleteLinkPayments'
            LINK_EXISTING_PLAYMENT = 'cp/finance/paymentOrderLink'
            REFUND_PAYMENT = 'cp/finance/paymentRefund'
            GET_RECEIPTS = 'komtet/getChecks'
            GET_PAYMENTS_SETTINGS = 'cp/payments/getPaymentMethodSettings'

        class Users:
            GET_USERS_LIST = 'cp/users'
            CREATE_USER = 'cp/user/new'
            GET_PROFILES = 'cp/users/profiles'
            EDIT_PROFILE = 'cp/users/profile'

            EDIT_USER = 'cp/user'

            GET_USER_SHIPMENT_ADDRESS = 'cp/user/shipmentAddresses'
            # Garage
            GET_USERS_CARS = 'cp/garage'
            SMS_SETTINGS = 'cp/user/smsSettings'

        class Staff:
            GET_STAFF = 'cp/managers'

        class Statuses:
            GET_STATUSES = 'cp/statuses'

        # Brand directory
        class Articles:
            GET_BRANDS = 'cp/articles/brands'
            GET_BRANDS_GROUP = 'cp/articles/brandsGroup'

        # Suppliers
        class Distributors:
            GET_DISTRIBUTORS_LIST = 'cp/distributors'
            EDIT_DISTRIBUTORS_STATUS = 'cp/distributor/status'
            UPLOAD_PRICE = 'cp/distributor/pricelistUpdate'

            GET_SUPPLIER_ROUTES = 'cp/routes'
            UPDATE_ROUTE = 'cp/route'
            UPDATE_ROUTE_STATUS = 'cp/routes/status'
            DELETE_ROUTE = 'cp/route/delete'
            EDIT_SUPPLIER_STATUS_FOR_OFFICE = 'cp/offices'
            GET_OFFICE_SUPPLIERS = 'cp/offices'

        class Catalog:
            INFO = f'cp/catalog/info'
            SEARCH = f'cp/catalog/search'
            INFO_BATCH = f'cp/catalog/info/batch'

    class Client:
        # SEARCH METHODS
        class Search:
            BRANDS = 'search/brands'
            ARTICLES = 'search/articles'
            BATCH = 'search/batch'
            HISTORY = 'search/history'
            TIPS = 'search/tips'
            ADVICES = 'advices'
            ADVICES_BATCH = 'advices/batch'

        # BASKET METHODS
        class Basket:
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

        class Orders:
            ORDERS_INSTANT = 'orders/instant'
            GET_ORDERS_LIST = 'orders/list'
            GET_ORDERS = 'orders'
            CANCEL_POSITION = 'orders/cancelPosition'

        class User:
            REGISTER = 'user/new'
            ACTIVATION = 'user/activation'
            USER_INFO = 'user/info'
            USER_RESTORE = 'user/restore'

        class Garage:
            USER_GARAGE = 'user/garage'
            GARAGE_CAR = 'user/garage/car'
            GARAGE_ADD = 'user/garage/add'
            GARAGE_UPDATE = 'user/garage/update'
            GARAGE_DELETE = 'user/garage/delete'

        class CarTree:
            CAR_TREE_YEARS = 'cartree/years'
            CAR_TREE_MANUFACTURERS = 'cartree/manufacturers'
            CAR_TREE_MODELS = 'cartree/models'
            CAR_TREE_MODIFICATIONS = 'cartree/modifications'

        class Form:
            FIELDS = 'form/fields'

        class Articles:
            BRANDS = 'articles/brands'
            INFO = 'articles/info'

    class TsClient:
        class GoodReceipts:
            CREATE = 'ts/goodReceipts/create'
            GET = 'ts/goodReceipts/get'
            GET_POSITIONS = 'ts/goodReceipts/getPositions'

        class OrderPickings:
            GET = 'ts/orderPickings/get'
            GET_POSITIONS = 'ts/orderPickings/getGoods'

        class CustomerComplaints:
            GET = 'ts/customerComplaints/get'
            GET_POSITIONS = 'ts/customerComplaints/getPositions'
            CREATE = 'ts/customerComplaints/create'
            UPDATE = 'ts/customerComplaints/updatePosition'
            CANCEL = 'ts/customerComplaints/cancelPosition'

        class Orders:
            CREATE = 'ts/orders/createByCart'
            GET_LIST = 'ts/orders/list'
            GET = 'ts/orders/get'
            REFUSE = 'ts/orders/refuse'

        class Cart:
            CREATE = 'ts/cart/create'
            UPDATE = 'ts/cart/update'
            GET_LIST = 'ts/cart/list'
            EXIST = 'ts/cart/exists'
            SUMMARY = 'ts/cart/summary'
            CLEAR = 'ts/cart/clear'
            DELETE = 'ts/cart/deletePositions'

        class Positions:
            GET = 'ts/positions/get'
            GET_LIST = 'ts/positions/list'
            CANCEL = 'ts/positions/cancel'
            MASS_CANCEL = 'ts/positions/massCancel'

    class TsAdmin:
        class OrderPickings:
            FAST_GET_OUT = 'cp/ts/orderPickings/fastGetOut'
            GET = 'cp/ts/orderPickings/get'
            GET_GOODS = '/cp/ts/orderPickings/getGoods'
            CREATE_BY_OLD_POS = '/cp/ts/orderPickings/createByOldPos'
            CHANGE_STATUS = '/cp/ts/orderPickings/changeStatus'
            UPDATE = '/cp/ts/orderPickings/update'
            DELETE_POSITION = '/cp/ts/orderPickings/deletePosition'

        class CustomerComplaints:
            GET = 'cp/ts/customerComplaints/get'
            GET_POSITIONS = '/cp/ts/customerComplaints/getPositions'
            CREATE = 'cp/ts/customerComplaints/create'
            CREATE_POSITION = 'cp/ts/customerComplaints/createPosition'
            UPDATE_POSITION = 'cp/ts/customerComplaints/updatePosition'
            CHANGE_STATUS_POSITION = 'cp/ts/customerComplaints/changeStatusPosition'
            UPDATE = 'cp/ts/customerComplaints/update'

        class DistributorOwners:
            DISTRIBUTOR_OWNERS = 'cp/ts/distributorOwners'

        class Orders:
            CREATE = 'cp/ts/orders/create'
            CREATE_BY_CART = 'cp/ts/orders/createByCart'
            LIST = 'cp/ts/orders/list'
            GET = 'cp/ts/orders/get'
            REFUSE = 'cp/ts/orders/refuse'
            UPDATE = 'cp/ts/orders/update'
            MERGE = 'cp/ts/orders/merge'
            SPLIT = 'cp/ts/orders/split'
            REPRICE = 'cp/ts/orders/reprice'
            MESSAGES_CREATE = 'cp/ts/orders/messages/create'
            MESSAGES_GET_ONE = 'cp/ts/orders/messages/get'
            MESSAGES_LIST = 'cp/ts/orders/messages/list'
            MESSAGES_UPDATE = 'cp/ts/orders/messages/update'
            MESSAGES_DELETE = 'cp/ts/orders/messages/delete'

        class Cart:
            CREATE = 'cp/ts/cart/create'
            UPDATE = 'cp/ts/cart/update'
            GET_LIST = 'cp/ts/cart/list'
            EXIST = 'cp/ts/cart/exists'
            SUMMARY = 'cp/ts/cart/summary'
            CLEAR = 'cp/ts/cart/clear'
            DELETE = 'cp/ts/cart/delete'
            TRANSFER = 'cp/ts/cart/transfer'

        class Positions:
            GET = 'cp/ts/positions/get'
            GET_LIST = 'cp/ts/positions/list'
            CREATE = 'cp/ts/positions/create'
            UPDATE = 'cp/ts/positions/update'
            CANCEL = 'cp/ts/positions/cancel'
            MASS_CANCEL = 'cp/ts/positions/massCancel'
            CHANGE_STATUS = 'cp/ts/positions/changeStatus'
            SPLIT = 'cp/ts/positions/split'
            MERGE = 'cp/ts/positions/merge'
            MESSAGES_LIST = 'cp/ts/positions/message/list'
            MESSAGES_GET = 'cp/ts/positions/message/get'
            MESSAGES_CREATE = 'cp/ts/positions/message/create'
            MESSAGES_UPDATE = 'cp/ts/positions/message/update'
            MESSAGES_DELETE = 'cp/ts/positions/message/delete'

        class GoodReceipts:
            CREATE = 'cp/ts/goodReceipts/create'
            GET = 'cp/ts/goodReceipts/get'
            GET_POSITIONS = 'cp/ts/goodReceipts/getPositions'
            UPDATE = 'cp/ts/goodReceipts/update'
            CHANGE_STATUS = 'cp/ts/goodReceipts/changeStatus'
            DELETE = 'cp/ts/goodReceipts/delete'

            CREATE_POSITION = 'cp/ts/goodReceipts/createPosition'
            DELETE_POSITION = 'cp/ts/goodReceipts/deletePosition'
            GET_POSITION = 'cp/ts/goodReceipts/getPosition'
            UPDATE_POSITION = 'cp/ts/goodReceipts/updatePosition'

    class Vinqu:
        pass

    class TecDoc:
        pass


SEARCH_METHODS = [Methods.Client.Search.BRANDS, Methods.Client.Search.ARTICLES, Methods.Client.Search.BATCH,
                  Methods.Client.Search.HISTORY, Methods.Client.Search.TIPS, Methods.Client.Search.ADVICES,
                  Methods.Client.Search.ADVICES_BATCH]
