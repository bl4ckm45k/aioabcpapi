DEFAULT_FILTER = ['self', 'cls']


def generate_payload(exclude=None, order: bool = False, **kwargs):
    """
    Generate payload
    :param exclude:
    :param order: Generate dict for create or edit order
    :param kwargs:
    :return: dict
    """
    if exclude is None:
        exclude = ['order_positions', 'order_params', 'online_positions', 'distributors', 'note', 'basket_positions']
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
        if value is not None:
            if key == 'order_positions':
                for z in range(len(value)):
                    for key_z, value_z in value[z].items():
                        data[f'order[positions][{z}][{key_z}]'] = value_z
            if key == 'order_params':
                for key_z, value_z in value[0].items():
                    data[f'orderParams[{key_z}]'] = value_z
            if key == 'online_positions':
                for z in range(len(value)):
                    for key_z, value_z in value[z].items():
                        data[f'positions[{z}][positionParams][{key_z}]'] = value_z
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
                        f"payments[0][{''.join([key.split('_')[0].lower(), *map(str.title, key.split('_')[1:])])}]"] = value
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
