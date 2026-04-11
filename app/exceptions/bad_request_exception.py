from app.exceptions.api_exception import APIException

class BadRequestException(APIException):
    def __init__(self, message="Bad request"):
        super().__init__(message, 400)