from app.exceptions.api_exception import APIException

class NotFoundException(APIException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)