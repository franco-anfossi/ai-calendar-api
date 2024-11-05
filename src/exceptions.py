from fastapi import HTTPException, status


class ResourceNotFound(HTTPException):
    def __init__(self, resource: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{resource} not found."
        )


class InvalidCredentials(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionDenied(HTTPException):
    def __init__(
        self, message: str = "You do not have permission to perform this action."
    ):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)
