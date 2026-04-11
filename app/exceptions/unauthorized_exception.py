from app.exceptions.api_exception import APIException

class UnauthorizedException(APIException):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)