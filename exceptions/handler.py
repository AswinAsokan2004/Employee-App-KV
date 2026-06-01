from fastapi.responses import JSONResponse

from exceptions.exceptions import (
    AppException,
    NotFoundException,
    ConflictException,
    BadRequestException,
    UnAutherizedException,
)
from fastapi import FastAPI, Request, status

_STATUS_MAP: dict[type[AppException], int] = {
    NotFoundException: status.HTTP_404_NOT_FOUND,
    ConflictException: status.HTTP_409_CONFLICT,
    BadRequestException: status.HTTP_400_BAD_REQUEST,
    UnAutherizedException: status.HTTP_401_UNAUTHORIZED,
}


def register_exception_handler(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: NotFoundException
    ) -> JSONResponse:
        code = _STATUS_MAP.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JSONResponse(status_code=code, content={"details": str(exc)})
