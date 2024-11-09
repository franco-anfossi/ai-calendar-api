from fastapi import HTTPException, status


class ResourceNotFound(HTTPException):
    def __init__(self, resource: str, message: str = None):
        detail = message if message else f"{resource} not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ResourceConflict(HTTPException):
    def __init__(self, resource: str, message: str = None):
        detail = message if message else f"{resource} already exists."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidDataError(HTTPException):
    def __init__(self, message: str = "Invalid data provided."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message
        )


class DatabaseError(HTTPException):
    def __init__(self, message: str = "A database error occurred."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
        )
