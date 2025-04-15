from typing import Optional, Any, Dict, Union


class AbcpBaseException(Exception):
    """Базовый класс для всех исключений ABCP API."""
    
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message or self.__class__.__name__


class UnsupportedHost(AbcpBaseException):
    """Исключение, возникающее при использовании неподдерживаемого хоста."""
    
    def __init__(self, host: str | None = None):
        message = f"Неподдерживаемый хост: {host}" if host else "Неподдерживаемый хост"
        super().__init__(message)


class UnsupportedLogin(AbcpBaseException):
    """Исключение, возникающее при использовании неподдерживаемого логина."""
    
    def __init__(self, login: str | None = None):
        message = f"Неподдерживаемый логин: {login}" if login else "Неподдерживаемый логин"
        super().__init__(message)


class PasswordType(AbcpBaseException):
    """Исключение, возникающее при использовании неверного типа пароля."""
    
    def __init__(self):
        super().__init__("Пароль должен быть строкой в формате MD5 хеша")


class NotEnoughRights(AbcpBaseException):
    """Исключение, возникающее при недостаточных правах для выполнения операции."""
    
    def __init__(self, message: str | None = None):
        super().__init__(message or "Недостаточно прав для выполнения операции")


class NetworkError(AbcpBaseException):
    """Исключение, возникающее при ошибках сети."""
    
    def __init__(self, message: str | None = None):
        super().__init__(message or "Сетевая ошибка при выполнении запроса")


class AbcpAPIError(AbcpBaseException):
    """Исключение, возникающее при ошибках API ABCP."""
    
    def __init__(self, message: str | None = None, error_code: str | None = None, 
                 status_code: int | None = None, data: Optional[Dict[str, Any]] = None):
        self.error_code = error_code
        self.status_code = status_code
        self.data = data
        
        error_info = []
        if message:
            error_info.append(message)
        if error_code:
            error_info.append(f"Код ошибки: {error_code}")
        if status_code:
            error_info.append(f"HTTP статус: {status_code}")
            
        super().__init__(" | ".join(error_info) if error_info else "Ошибка API ABCP")


class AbcpParameterRequired(AbcpBaseException):
    """Исключение, возникающее при отсутствии обязательного параметра."""
    
    def __init__(self, parameter: str):
        super().__init__(f"Отсутствует обязательный параметр: {parameter}")


class AbcpWrongParameterError(AbcpBaseException):
    """Исключение, возникающее при неверном значении параметра."""
    
    def __init__(self, parameter: str, value: Any, expected: Optional[Union[type, str]] = None):
        message = f"Неверное значение параметра '{parameter}': {value}"
        if expected:
            message += f", ожидается: {expected}"
        super().__init__(message)


class TeaPot(AbcpBaseException):
    """Исключение для статуса 418 - I'm a teapot."""
    
    def __init__(self):
        super().__init__("I'm a teapot (RFC 2324)")


class AbcpNotFoundError(AbcpBaseException):
    """Исключение, возникающее при отсутствии запрашиваемого ресурса."""
    
    def __init__(self, resource: str | None = None):
        message = f"Ресурс не найден: {resource}" if resource else "Ресурс не найден"
        super().__init__(message)


class FileSizeExceeded(AbcpBaseException):
    """Исключение, возникающее при превышении допустимого размера файла."""
    
    def __init__(self, max_size: int | None = None):
        message = f"Превышен допустимый размер файла"
        if max_size:
            message += f": максимальный размер {max_size} байт"
        super().__init__(message)
