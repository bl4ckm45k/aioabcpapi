from dataclasses import dataclass

from environs import Env


@dataclass
class Abcp:
    host: str
    login: str
    password: str


@dataclass
class Config:
    abcp: Abcp


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        abcp=Abcp(
            host=env.str('ABCP_HOST'),
            login=env.str('ABCP_LOGIN'), password=env.str('ABCP_PASSWORD')
        ))
