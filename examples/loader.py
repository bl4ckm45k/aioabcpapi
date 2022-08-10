from aioabcpapi.abcp import Abcp
from examples.config import host, login, password, login_user, password_user

api = Abcp(host, login, password)

api_client = Abcp(host, login_user, password_user)
