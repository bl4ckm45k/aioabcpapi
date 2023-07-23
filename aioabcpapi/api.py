import logging
import re
from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, Union

import aiohttp

from .exceptions import UnsupportedHost, PasswordType, UnsupportedLogin, NetworkError, \
    AbcpAPIError, TeaPot, AbcpNotFoundError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


def check_data(host: str, login: str, password: str) -> bool:
    regex_md = re.match(r"([a-f\d]{32})", password)
    if not regex_md:
        raise PasswordType('Допускаются пароли только в md5 hash')
    host_id = host.split('.')[0]
    if login[0:4] == 'api@':
        return login.split('@')[1] == host_id
    if host_id[2:].isdigit() and len(host_id) < 10 and host[0:2] == 'id':
        if login.isdigit() and 4 < len(login) < 14:
            return False
        if '@' in login:
            email = re.match('^[\w.]+@([\w-]+\.)+[\w-]{2,6}$', login, flags=re.IGNORECASE)
            if not email:
                raise UnsupportedLogin('Недопустимый логин')
            return False
        raise UnsupportedLogin('Недопустимый логин')
    else:
        raise UnsupportedHost(f'Имя хоста {host} не поддерживается\n'
                              f'Допустимые имена:\n'
                              f'id200.public.api.abcp.ru\n'
                              f'abcp55333.public.api.abcp.ru')


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
    elif status_code == 418:
        raise TeaPot("RFC 2324, секция 2.3.2: 418 I'm a teapot")

    raise AbcpAPIError(f"{body} [{status_code}]")


async def make_request_json(session, host, method,
                            data: Dict, headers,
                            **kwargs):
    url = f'https://{host}/{method}'
    try:
        async with session.post(url, json=data, headers=headers, **kwargs) as response:
            try:
                body = await response.json()
                return check_result(method, response.content_type, response.status, body)
            except:
                raise AbcpAPIError(response.text)
    except aiohttp.ClientError as e:
        raise NetworkError(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")


async def make_request(session, host, method,
                       data: Union[Dict, aiohttp.FormData],
                       headers, post,
                       **kwargs):
    logger.debug('Make _request: "%s" with data: "%r"', method, data)

    url = f'https://{host}/{method}'
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


class Headers:
    __json_header = {'Content-Type': 'application/json',
                     'Accept': 'application/json'}
    __url_encoded_header = {'Content-Type': 'application/x-www-form-urlencoded',
                            'Accept': 'application/json'}
    __multipart_header = None

    def __init__(self):
        pass

    def json_header(self):
        return self.__json_header

    def url_encoded_header(self):
        return self.__url_encoded_header

    def multipart_header(self):
        return self.__multipart_header


class _Methods:
    class Admin:
        @dataclass(frozen=True)
        class Orders:
            GET_ORDERS_LIST: str = 'cp/orders'
            GET_ORDER: str = 'cp/order'
            STATUS_HISTORY: str = 'cp/order/statusHistory'
            SAVE_ORDER: str = 'cp/order'
            ONLINE_ORDER: str = 'cp/orders/online'

        @dataclass(frozen=True)
        class Finance:
            UPDATE_BALANCE: str = 'cp/finance/userBalance'
            UPDATE_CREDIT_LIMIT: str = 'cp/finance/creditLimit'
            UPDATE_FINANCE_INFO: str = 'cp/finance/userInfo'
            GET_PAYMENTS: str = 'cp/finance/payments'
            GET_PAYMENTS_LINKS: str = 'cp/finance/paymentOrderLinks'
            GET_PAYMENTS_ONLINE: str = 'cp/onlinePayments'
            ADD_PAYMENTS: str = 'cp/finance/payments'
            DELETE_PAYMENT_LINK: str = 'cp/finance/deleteLinkPayments'
            LINK_EXISTING_PLAYMENT: str = 'cp/finance/paymentOrderLink'
            REFUND_PAYMENT: str = 'cp/finance/paymentRefund'
            GET_RECEIPTS: str = 'komtet/getChecks'
            GET_PAYMENTS_SETTINGS: str = 'cp/payments/getPaymentMethodSettings'
            DELETE_PAYMENT: str = 'cp/finance/deletePayments'

        @dataclass(frozen=True)
        class Users:
            GET_USERS_LIST: str = 'cp/users'
            CREATE_USER: str = 'cp/user/new'
            GET_PROFILES: str = 'cp/users/profiles'
            EDIT_PROFILE: str = 'cp/users/profile'

            EDIT_USER: str = 'cp/user'

            GET_USER_SHIPMENT_ADDRESS: str = 'cp/user/shipmentAddresses'
            GET_USER_SHIPMENT_ADDRESS_ZONES: str = 'cp/user/shipmentAddressZones'
            GET_USER_SHIPMENT_ADDRESS_ZONE: str = 'cp/user/shipmentAddressZones/{}'
            UPDATE_SHIPMENT_ZONES: str = 'cp/user/shipmentAddressZones'
            CREATE_SHIPMENT_ZONE: str = 'cp/user/shipmentAddressZones/new'
            UPDATE_SHIPMENT_ZONE: str = 'cp/user/shipmentAddressZones/{}/update'
            DELETE_SHIPMENT_ZONE: str = 'cp/user/shipmentAddress/{}/delete'
            # Garage
            GET_USERS_CARS: str = 'cp/garage'
            SMS_SETTINGS: str = 'cp/user/smsSettings'

        @dataclass(frozen=True)
        class Staff:
            GET_STAFF: str = 'cp/managers'
            UPDATE_STAFF: str = 'cp/manager'

        @dataclass(frozen=True)
        class Statuses:
            GET_STATUSES: str = 'cp/statuses'

        @dataclass(frozen=True)
        class Articles:
            GET_BRANDS: str = 'cp/articles/brands'
            GET_BRANDS_GROUP: str = 'cp/articles/brandsGroup'

        @dataclass(frozen=True)
        class Distributors:
            GET_DISTRIBUTORS_LIST: str = 'cp/distributors'
            EDIT_DISTRIBUTORS_STATUS: str = 'cp/distributor/status'
            UPLOAD_PRICE: str = 'cp/distributor/pricelistUpdate'

            GET_SUPPLIER_ROUTES: str = 'cp/routes'
            UPDATE_ROUTE: str = 'cp/route'
            UPDATE_ROUTE_STATUS: str = 'cp/routes/status'
            DELETE_ROUTE: str = 'cp/route/delete'
            EDIT_SUPPLIER_STATUS_FOR_OFFICE: str = 'cp/offices'
            GET_OFFICE_SUPPLIERS: str = 'cp/offices'

        @dataclass(frozen=True)
        class Catalog:
            INFO = f'cp/catalog/info'
            SEARCH = f'cp/catalog/search'
            INFO_BATCH = f'cp/catalog/info/batch'

        @dataclass(frozen=True)
        class UsersCatalog:
            UPLOAD: str = 'cp/usercatalogs/{}/upload'

        @dataclass(frozen=True)
        class Payment:
            TOKEN: str = 'cp/payment/token'
            TOP_BALANCE: str = 'cp/payment/top-balance-link'

    class Client:
        # SEARCH METHODS
        @dataclass(frozen=True)
        class Search:
            BRANDS: str = 'search/brands'
            ARTICLES: str = 'search/articles'
            BATCH: str = 'search/batch'
            HISTORY: str = 'search/history'
            TIPS: str = 'search/tips'
            ADVICES: str = 'advices'
            ADVICES_BATCH: str = 'advices/batch'

        # BASKET METHODS
        @dataclass(frozen=True)
        class Basket:
            BASKETS_LIST: str = 'basket/multibasket'
            BASKET_ADD: str = 'basket/add'
            BASKET_CLEAR: str = 'basket/clear'
            BASKET_CONTENT: str = 'basket/content'
            BASKET_OPTIONS: str = 'basket/options'
            PAYMENT_METHODS: str = 'basket/paymentMethods'
            SHIPMENT_METHOD: str = 'basket/shipmentMethods'
            SHIPMENT_OFFICES: str = 'basket/shipmentOffices'
            SHIPMENT_ADDRESS: str = 'basket/shipmentAddresses'
            SHIPMENT_DATES: str = 'basket/shipmentDates'
            BASKET_ORDER: str = 'basket/order'

        @dataclass(frozen=True)
        class Orders:
            ORDERS_INSTANT: str = 'orders/instant'
            GET_ORDERS_LIST: str = 'orders/list'
            GET_ORDERS: str = 'orders'
            CANCEL_POSITION: str = 'orders/cancelPosition'

        @dataclass(frozen=True)
        class User:
            REGISTER: str = 'user/new'
            ACTIVATION: str = 'user/activation'
            USER_INFO: str = 'user/info'
            USER_RESTORE: str = 'user/restore'

        @dataclass(frozen=True)
        class Garage:
            USER_GARAGE: str = 'user/garage'
            GARAGE_CAR: str = 'user/garage/car'
            GARAGE_ADD: str = 'user/garage/add'
            GARAGE_UPDATE: str = 'user/garage/update'
            GARAGE_DELETE: str = 'user/garage/delete'

        @dataclass(frozen=True)
        class CarTree:
            CAR_TREE_YEARS: str = 'cartree/years'
            CAR_TREE_MANUFACTURERS: str = 'cartree/manufacturers'
            CAR_TREE_MODELS: str = 'cartree/models'
            CAR_TREE_MODIFICATIONS: str = 'cartree/modifications'

        @dataclass(frozen=True)
        class Form:
            FIELDS: str = 'form/fields'

        @dataclass(frozen=True)
        class Articles:
            BRANDS: str = 'articles/brands'
            INFO: str = 'articles/info'

    class TsClient:
        @dataclass(frozen=True)
        class GoodReceipts:
            CREATE: str = 'ts/goodReceipts/create'
            GET: str = 'ts/goodReceipts/get'
            GET_POSITIONS: str = 'ts/goodReceipts/getPositions'

        @dataclass(frozen=True)
        class OrderPickings:
            GET: str = 'ts/orderPickings/get'
            GET_POSITIONS: str = 'ts/orderPickings/getGoods'

        @dataclass(frozen=True)
        class CustomerComplaints:
            GET: str = 'ts/customerComplaints/get'
            GET_POSITIONS: str = 'ts/customerComplaints/getPositions'
            CREATE: str = 'ts/customerComplaints/create'
            CREATE_POSITION_MULTIPLE: str = 'ts/customerComplaints/createPositionMultiple'
            UPDATE: str = 'ts/customerComplaints/updatePosition'
            CANCEL: str = 'ts/customerComplaints/cancelPosition'

        @dataclass(frozen=True)
        class Orders:
            CREATE: str = 'ts/orders/createByCart'
            GET_LIST: str = 'ts/orders/list'
            GET: str = 'ts/orders/get'
            REFUSE: str = 'ts/orders/refuse'

        @dataclass(frozen=True)
        class Cart:
            CREATE: str = 'ts/cart/create'
            UPDATE: str = 'ts/cart/update'
            GET_LIST: str = 'ts/cart/list'
            EXIST: str = 'ts/cart/exists'
            SUMMARY: str = 'ts/cart/summary'
            CLEAR: str = 'ts/cart/clear'
            DELETE: str = 'ts/cart/deletePositions'

        @dataclass(frozen=True)
        class Positions:
            GET: str = 'ts/positions/get'
            GET_LIST: str = 'ts/positions/list'
            CANCEL: str = 'ts/positions/cancel'
            MASS_CANCEL: str = 'ts/positions/massCancel'

        @dataclass(frozen=True)
        class Agreements:
            get_list: str = 'cp/ts/agreements/list'

    @dataclass(frozen=True)
    class TsAdmin:
        @dataclass(frozen=True)
        class OrderPickings:
            FAST_GET_OUT: str = 'cp/ts/orderPickings/fastGetOut'
            GET: str = 'cp/ts/orderPickings/get'
            GET_GOODS: str = 'cp/ts/orderPickings/getGoods'
            CREATE_BY_OLD_POS: str = 'cp/ts/orderPickings/createByOldPos'
            CHANGE_STATUS: str = 'cp/ts/orderPickings/changeStatus'
            UPDATE: str = 'cp/ts/orderPickings/update'
            DELETE_POSITION: str = 'cp/ts/orderPickings/deletePosition'

        @dataclass(frozen=True)
        class CustomerComplaints:
            GET: str = 'cp/ts/customerComplaints/get'
            GET_POSITIONS: str = 'cp/ts/customerComplaints/getPositions'
            CREATE: str = 'cp/ts/customerComplaints/create'
            CREATE_POSITION: str = 'cp/ts/customerComplaints/createPosition'
            CREATE_POSITION_MULTIPLE: str = 'cp/ts/customerComplaints/createPositionMultiple'
            UPDATE_POSITION: str = 'cp/ts/customerComplaints/updatePosition'
            CHANGE_STATUS_POSITION: str = 'cp/ts/customerComplaints/changeStatusPosition'
            UPDATE: str = 'cp/ts/customerComplaints/update'
            UPDATE_CUSTOM_FILE: str = 'cp/ts/customerComplaints/updateCustomFile'

        class SupplierReturns:
            @dataclass
            class Operations:
                __section: str = '/cp/ts/supplierReturns/operations'
                LIST: str = f'{__section}/list'
                SUM: str = f'{__section}/sum'
                GET: str = f'{__section}/get'
                CREATE: str = f'{__section}/create'
                UPDATE: str = f'{__section}/update'
                DELETE: str = f'{__section}/delete'

            @dataclass
            class Positions:
                __section: str = '/cp/ts/supplierReturns/positions'
                LIST: str = f'{__section}/list'
                SUM: str = f'{__section}/sum'
                STATUS: str = f'{__section}/status'
                GET: str = f'{__section}/get'
                CREATE_MULTIPLE: str = f'{__section}/createMultiple'
                SPLIT = f'{__section}/split'
                UPDATE = f'{__section}/update'
                CHANGE_STATUS = f'{__section}/changeStatus'

            @dataclass
            class PositionsAttr:
                __section: str = '/cp/ts/supplierReturns/positions/attr'
                CREATE: str = f'{__section}/create'
                UPDATE: str = f'{__section}/update'
                DELETE: str = f'{__section}/delete'

        @dataclass(frozen=True)
        class DistributorOwners:
            DISTRIBUTOR_OWNERS: str = 'cp/ts/distributorOwners'

        @dataclass(frozen=True)
        class Orders:
            __section: str = 'cp/ts/orders'
            CREATE: str = f'{__section}/create'
            CREATE_BY_CART: str = f'{__section}/createByCart'
            LIST: str = f'{__section}/list'
            GET: str = f'{__section}/get'
            REFUSE: str = f'{__section}/refuse'
            UPDATE: str = f'{__section}/update'
            MERGE: str = f'{__section}/merge'
            SPLIT: str = f'{__section}/split'
            REPRICE: str = f'{__section}/reprice'
            MESSAGES_CREATE: str = f'{__section}/messages/create'
            MESSAGES_GET_ONE: str = f'{__section}/messages/get'
            MESSAGES_LIST: str = f'{__section}/messages/list'
            MESSAGES_UPDATE: str = f'{__section}/messages/update'
            MESSAGES_DELETE: str = f'{__section}/messages/delete'

        @dataclass(frozen=True)
        class Cart:
            CREATE: str = 'cp/ts/cart/create'
            UPDATE: str = 'cp/ts/cart/update'
            GET_LIST: str = 'cp/ts/cart/list'
            EXIST: str = 'cp/ts/cart/exists'
            SUMMARY: str = 'cp/ts/cart/summary'
            CLEAR: str = 'cp/ts/cart/clear'
            DELETE: str = 'cp/ts/cart/delete'
            TRANSFER: str = 'cp/ts/cart/transfer'

        @dataclass(frozen=True)
        class Positions:
            GET: str = 'cp/ts/positions/get'
            GET_LIST: str = 'cp/ts/positions/list'
            CREATE: str = 'cp/ts/positions/create'
            UPDATE: str = 'cp/ts/positions/update'
            CANCEL: str = 'cp/ts/positions/cancel'
            MASS_CANCEL: str = 'cp/ts/positions/massCancel'
            CHANGE_STATUS: str = 'cp/ts/positions/changeStatus'
            SPLIT: str = 'cp/ts/positions/split'
            MERGE: str = 'cp/ts/positions/merge'
            MESSAGES_LIST: str = 'cp/ts/positions/message/list'
            MESSAGES_GET: str = 'cp/ts/positions/message/get'
            MESSAGES_CREATE: str = 'cp/ts/positions/message/create'
            MESSAGES_UPDATE: str = 'cp/ts/positions/message/update'
            MESSAGES_DELETE: str = 'cp/ts/positions/message/delete'

        @dataclass(frozen=True)
        class GoodReceipts:
            CREATE: str = 'cp/ts/goodReceipts/create'
            GET: str = 'cp/ts/goodReceipts/get'
            GET_POSITIONS: str = 'cp/ts/goodReceipts/getPositions'
            UPDATE: str = 'cp/ts/goodReceipts/update'
            CHANGE_STATUS: str = 'cp/ts/goodReceipts/changeStatus'
            DELETE: str = 'cp/ts/goodReceipts/delete'

            CREATE_POSITION: str = 'cp/ts/goodReceipts/createPosition'
            DELETE_POSITION: str = 'cp/ts/goodReceipts/deletePosition'
            GET_POSITION: str = 'cp/ts/goodReceipts/getPosition'
            UPDATE_POSITION: str = 'cp/ts/goodReceipts/updatePosition'

        @dataclass(frozen=True)
        class Tags:
            LIST: str = 'cp/ts/tags/list'
            CREATE: str = 'cp/ts/tags/create'
            DELETE: str = 'cp/ts/tags/delete'

        @dataclass(frozen=True)
        class TagsRelationships:
            LIST: str = 'cp/ts/tagsRelationships/list'
            CREATE: str = 'cp/ts/tagsRelationships/create'
            DELETE: str = 'cp/ts/tagsRelationships/delete'

        @dataclass(frozen=True)
        class Payments:
            GET_LIST: str = 'cp/ts/payments/list'
            CREATE: str = 'cp/ts/payments/create'

        @dataclass(frozen=True)
        class PaymentMethods:
            METHODS_LIST: str = 'cp/ts/paymentMethods/list'

        @dataclass(frozen=True)
        class Agreements:
            get_list: str = 'cp/ts/agreements/list'

        @dataclass(frozen=True)
        class LegalPersons:
            get_list: str = 'cp/ts/legalPersons/list'

    class VinQu:
        pass

    class TecDoc:
        pass


SEARCH_METHODS = (_Methods.Client.Search.BRANDS, _Methods.Client.Search.ARTICLES, _Methods.Client.Search.BATCH,
                  _Methods.Client.Search.HISTORY, _Methods.Client.Search.TIPS, _Methods.Client.Search.ADVICES,
                  _Methods.Client.Search.ADVICES_BATCH)
