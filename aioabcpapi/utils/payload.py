import logging
import os
from io import BufferedReader

from aiohttp import FormData

from aioabcpapi.exceptions import FileSizeExceeded

DEFAULT_FILTER = ['self', 'cls', 'kwargs']
logger = logging.getLogger('utils/payload')


def get_pascal_case_key(key: str):
    return ''.join([*map(str.title, key.split('_'))])


def get_camel_case_key(key: str):
    return f"{''.join([key.split('_')[0].lower(), *map(str.title, key.split('_')[1:])])}"


def get_excluded_keys(key: str):
    excluded_keys = {
        'order_positions': 'order[positions][_index_][_key_]',
        'positions': 'positions[_index_][_key_]',
        'articles_catalog': 'articles[_index_][_key_]',
        'properties': 'properties[_key_][_index_]',
        'order_params': 'orderParams[_key_]',
        'distributors': 'distributors[_index_][_key_]',
        'search': 'search[_index_][_key_]',
        'basket_positions': 'positions[_index_][_key_]',
        'goods_group': 'goods_group',
        'note': 'order[notes][0][value]',
        'del_note': 'order[notes][0][value]',
        'delivery_address': 'delivery[meetData][address]',
        'delivery_person': 'delivery[meetData][person]',
        'delivery_contact': 'delivery[meetData][contact]',
        'delivery_comment': 'delivery[meetData][comment]',
        'delivery_employee_contact': 'delivery[meetData][employeeContact]',
        'delivery_employee_person': 'delivery[meetData][employeePerson]',
        'delivery_reseller_comment': 'delivery[meetData][resellerComment]',
        'delivery_start_time': 'delivery[timeInterval][startTime]',
        'delivery_end_time': 'delivery[timeInterval][endTime]',
        'delivery_method_id': 'delivery[methodId]',
        'client_order_number': 'clientOrderNumber',
        'cross_image': 'cross_image',
        'with_original': 'with_original',
        'old_item_id': 'oldItemID',
        'distributors_price_ups': 'distributorsPriceUps[_index_]',
        'matrix_price_ups': 'matrixPriceUps[_index_]',
    }
    try:
        return excluded_keys[key]
    except KeyError:
        return get_pascal_case_key(key)


def generate_payload(exclude=None, order: bool = False, **kwargs):
    """
    Generate payload
    :param exclude:
    :param order: Generate dict for create or edit order
    :param kwargs:
    :return: dict
    """
    if exclude is None:
        exclude = ['order_params', 'distributors', 'note', 'del_note',
                   'basket_positions', 'sip']
    data = {}

    for key, value in kwargs.items():
        if key not in exclude + DEFAULT_FILTER and value is not None and not key.startswith('_'):
            if not order:
                if isinstance(value, list):
                    for i, x in enumerate(value):
                        data[f"{get_camel_case_key(key)}[{i}]"] = x
                else:
                    data[get_camel_case_key(key)] = value
            else:
                data[f"order[{get_camel_case_key(key)}]"] = value
        if key in exclude and key not in DEFAULT_FILTER and value is not None:
            if isinstance(value, list):
                if key == 'articles':
                    data['articles'] = value
                elif key == 'reseller_data':
                    data['resellerData'] = value
                elif key in ('distributors_price_ups', 'matrix_price_ups'):
                    data = data | generate_price_ups(key, value)
                else:
                    data = {**data, **generate_from_list(key, value)}

            else:
                if key == 'sip':
                    data[key.upper()] = value
                if key == 'del_note':
                    data['order[notes][0][value]'] = None
                    data['order[notes][0][id]'] = value
                else:
                    data[get_excluded_keys(key)] = value
        if key == 'kwargs':
            for k, v, in value.items():
                data[get_camel_case_key(k)] = v
    logger.debug(f'{data}')
    return data


def generate_price_ups(key, value):
    data = {}
    for i in range(len(value)):
        for key_z, value_z in value[i].items():
            data_key = get_excluded_keys(key).replace('_index_', str(i)).replace('_key_', key_z)
            if isinstance(value_z, dict):
                list_keys = list(value_z.keys())
                for key_j, value_j in value_z.items():
                    index_key_j = list_keys.index(key_j)
                    data[f'{data_key}[{key_z}][{index_key_j}][name]'] = key_j
                    data[f'{data_key}[{key_z}][{index_key_j}][priceUp]'] = value_j
            else:
                data[f'{data_key}[{key_z}]'] = value_z
    logger.debug(f'{data}')
    return data


def generate_from_list(key, value):
    data = {}
    for i in range(len(value)):
        for key_z, value_z in value[i].items():
            if not isinstance(value_z, list):
                data_key = get_excluded_keys(key).replace('_index_', str(i)).replace('_key_', key_z)
                data[data_key] = value_z
            else:
                data_key = get_excluded_keys(key).replace('_index_', str(i)).replace('_key_', key_z)
                for index_j, value_j in enumerate(value_z):
                    data[f'{data_key}[{index_j}]'] = value_j
    logger.debug(f'{data}')
    return data


def generate_payload_filter(**kwargs):
    data = {}
    for key, value in kwargs.items():
        if key not in DEFAULT_FILTER and value is not None and not key.startswith('_'):
            if isinstance(value, list):
                for i, x in enumerate(value):
                    data[
                        f"filter[{get_camel_case_key(key)}][{i}]"] = x
            else:
                data[f"filter[{get_camel_case_key(key)}]"] = value
    logger.debug(f'{data}')
    return data


def generate_payload_payments(single: bool = True, **kwargs):
    data = {}
    for key, value in kwargs.items():
        if key not in DEFAULT_FILTER and value is not None and not key.startswith('_'):
            if single:
                if key == 'link_payments':
                    data['linkPayments'] = value
                else:
                    data[
                        f"payments[0][{get_camel_case_key(key)}]"
                    ] = value
            else:
                if isinstance(value, list):
                    for z in range(len(value)):
                        for key_z, value_z in value[z].items():
                            data[f'payments[{z}][{key_z}]'] = value_z
                else:
                    data[get_camel_case_key(key)] = value
    logger.debug(f'{data}')
    return data


def generate_payload_online_order(**kwargs):
    """
    Generate payload
    :param kwargs:
    :return: dict
    """
    data = {}
    for key, value in kwargs.items():
        if key not in DEFAULT_FILTER and value is not None and not key.startswith('_'):
            if key == 'order_params':
                for z in range(len(value)):
                    for key_z, value_z in value[0].items():
                        data[f'orderParams[{key_z}]'] = value_z
            if key == 'positions':
                for z in range(len(value)):
                    for key_z, value_z in value[z].items():
                        if key_z == 'id':
                            data[f'positions[{z}][{key_z}]'] = value_z
                        else:
                            data[f'positions[{z}][positionParams][{key_z}]'] = value_z
    logger.debug(f'{data}')
    return data


def generate_file_payload(exclude=None, max_size: int = None, **kwargs):
    """
    Generate payload
    :param exclude:
    :param max_size: Максимальный размер в Мб
    :param kwargs:
    :return: :obj:`aiohttp.FormData`
    """
    if exclude is None:
        exclude = []
    data = FormData()
    for key, value in kwargs.items():
        if key not in exclude + DEFAULT_FILTER and value is not None and not key.startswith('_'):
            data.add_field(get_camel_case_key(key), str(value))
        if key in exclude and key != '' and value is not None:
            if isinstance(value, BufferedReader):
                data.add_field(get_camel_case_key(key), value, filename=value.name, content_type='multipart/form-data')
            if isinstance(value, str) and not value.isdigit():
                with open(value, 'rb') as file:
                    if max_size is not None:
                        size = file.seek(0, os.SEEK_END)
                        if (size / 1_048_576) > max_size: raise FileSizeExceeded(
                            f'Файл не может быть больше {max_size} Мб')
                    data.add_field(get_camel_case_key(key), file, filename=file.name,
                                   content_type='multipart/form-data')
    logger.debug(f'{data}')
    return data
