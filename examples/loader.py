from aioabcpapi import Abcp
from examples.config import load_config

config = load_config()

api = Abcp(config.abcp.host, config.abcp.login, config.abcp.password)
