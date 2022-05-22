from aioabcpapi.cp.admin import AdminApi
from aioabcpapi.cp.client import ClientApi
from examples.config import host, login, password, login_user, password_user

api = AdminApi(host, login, password)
api_client = ClientApi(host, login_user, password_user)
