from aiohttp import FormData
import logging
from io import BufferedReader
DEFAULT_FILTER = ['self', 'cls']
logger = logging.getLogger(__name__)


def generate_payload(exclude=None, order: bool = False, **kwargs):
    """
    Generate payload
    :param exclude:
    :param order: Generate dict for create or edit order
    :param kwargs:
    :return: dict
    """
    if exclude is None:
        exclude = ['order_positions', 'order_params', 'distributors', 'note', 'del_note',
                   'basket_positions']
    data = dict()
    for key, value in kwargs.items():
        if key not in exclude + DEFAULT_FILTER and value is not None and not key.startswith('_'):
            if order is False:
                if type(value) is list:
                    for i, x in enumerate(value):
                        data[f"{''.join([key.split('_')[0].lower(), *map(str.title, key.split('_')[1:])])}[{i}]"] = x
                else:
                    data[''.join([key.split('_')[0].lower(), *map(str.title, key.split('_')[1:])])] = value
            else:
                data[f"order[{''.join([key.split('_')[0].lower(), *map(str.title, key.split('_')[1:])])}]"] = value
        if key in exclude and key not in DEFAULT_FILTER:
            if key == 'order_positions':
                for z in range(len(value)):
                    for key_z, value_z in value[z].items():
                        data[f'order[positions][{z}][{key_z}]'] = value_z
            if key == 'order_params':
                for key_z, value_z in value[0].items():
                    data[f'orderParams[{key_z}]'] = value_z
            if key == 'distributors':
                for z in range(len(value)):
                    for key_z, value_z in value[z].items():
                        data[f'{key}[{z}][{key_z}]'] = value_z
            if key == 'note':
                data[f'order[notes][0][value]'] = value
            if key == 'del_note':
                data[f'order[notes][0][value]'] = ''
                data[f'order[notes][0][id]'] = value
            if key == 'basket_positions':
                for z in range(len(value)):
                    for key_z, value_z in value[z].items():
                        data[f'positions[{z}][{key_z}]'] = value_z
            if key == 'search':
                for z in range(len(value)):
                    for key_z, value_z in value[z].items():
                        data[f'search[{z}][{key_z}]'] = value_z
            if key == 'articles':
                data['articles'] = value

    return data


def generate_payload_filter(**kwargs):
    data = dict()
    for key, value in kwargs.items():
        if key not in DEFAULT_FILTER and value is not None and not key.startswith('_'):
            if type(value) is list:
                for i, x in enumerate(value):
                    data[
                        f"filter[{''.join([key.split('_')[0].lower(), *map(str.title, key.split('_')[1:])])}][{i}]"] = x
            else:
                data[f"filter[{''.join([key.split('_')[0].lower(), *map(str.title, key.split('_')[1:])])}]"] = value
    return data


def generate_payload_payments(single: bool = True, **kwargs):
    data = dict()
    for key, value in kwargs.items():
        if key not in DEFAULT_FILTER and value is not None and not key.startswith('_'):
            if single:
                if key == 'link_payments':
                    data['linkPayments'] = value
                else:
                    data[
                        f"payments[0][{''.join([key.split('_')[0].lower(), *map(str.title, key.split('_')[1:])])}]"
                    ] = value
            else:
                for z in range(len(value)):
                    for key_z, value_z in value[z].items():
                        data[f'payments[{z}][{key_z}]'] = value_z
    return data


def generate_payload_online_order(**kwargs):
    """
    Generate payload
    :param kwargs:
    :return: dict
    """
    data = dict()
    for key, value in kwargs.items():
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
    return data


def generate_file_payload(exclude=None, **kwargs):
    """
    Generate payload
    :param exclude:
    :param kwargs:
    :return: dict
    """
    if exclude is None:
        exclude = []
    data = FormData()
    for key, value in kwargs.items():
        if key not in exclude + DEFAULT_FILTER and value is not None and not key.startswith('_'):
            data.add_field(''.join([key.split('_')[0].lower(), *map(str.title, key.split('_')[1:])]), str(value))
        if key in exclude and key != '':
            file_path = str(value).replace('\\', '/')
            if isinstance(value, BufferedReader):
                data.add_field('UploadFile', value, filename=value.name, content_type='multipart/form-data')
            else:
                data.add_field('uploadFile',
                               open(str(value), 'rb'),
                               filename=file_path.split('/')[-1], content_type='multipart/form-data')
    return data
