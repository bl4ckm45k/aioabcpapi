from aioabcpapi.exceptions import AbcpWrongParameterError


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
