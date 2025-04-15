from datetime import datetime

import pytz
from pyrfc3339.generator import generate

from aioabcpapi.exceptions import AbcpWrongParameterError
from functools import wraps


def check_fields(fields_to_check, fields_values):
    if isinstance(fields_to_check, str):
        if fields_to_check not in fields_values:
            raise AbcpWrongParameterError(
                f'Параметр "fields" может принимать значения {fields_values}\n'
                f'Для передачи нескольких параметров передавайте list')
        return fields_to_check
    if isinstance(fields_to_check, list):
        if all(x in fields_values for x in fields_to_check):
            return ','.join(fields_to_check)
        raise AbcpWrongParameterError(
            f'Параметр "fields" может принимать значения {fields_values}')


def check_limit(func):
    @wraps(func)
    async def wrapper(self, *args, limit=None, **kwargs):
        if limit is not None and not 1 <= limit <= 1000:
            raise AbcpWrongParameterError("limit", limit, "должен быть в диапазоне от 1 до 1000")
        return await func(self, *args, limit=limit, **kwargs)

    return wrapper


def process_ts_dates(*date_keys):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            for key in date_keys:
                if key in kwargs and isinstance(kwargs[key], datetime):
                    if isinstance(kwargs[key], datetime):
                        kwargs[key] = generate(kwargs[key].replace(tzinfo=pytz.utc))

            return await func(self, *args, **kwargs)

        return wrapper

    return decorator


def process_ts_lists(*list_keys):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            for key in list_keys:
                if key in kwargs and isinstance(kwargs[key], list):
                    if isinstance(kwargs[key], list):
                        kwargs[key] = ','.join(map(str, kwargs[key]))
            return await func(self, *args, **kwargs)

        return wrapper

    return decorator
