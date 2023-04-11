class UnsupportedHost(Exception):
    pass


class UnsupportedLogin(Exception):
    pass


class PasswordType(Exception):
    pass


class NotEnoughRights(Exception):
    pass


class NetworkError(Exception):
    pass


class AbcpAPIError(Exception):
    pass


class AbcpParameterRequired(Exception):
    pass


class AbcpWrongParameterError(Exception):
    pass


class TeaPot(Exception):
    pass


class AbcpNotFoundError(Exception):
    pass


class FileSizeExceeded(Exception):
    pass
