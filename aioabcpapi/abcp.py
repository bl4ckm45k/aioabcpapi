from aioabcpapi import BaseAbcp
from aioabcpapi.cp.base import CpApi
from aioabcpapi.ts.base import TsApi


class Abcp(BaseAbcp):
    def __init__(self, *args):
        super().__init__(*args)
        self.cp = CpApi(*args)
        self.ts = TsApi(*args)
