from app.exceptions.api_exception import APIException

class ConflictException(APIException):
    def __init__(self, message="Conflict"):
        super().__init__(message, 409)