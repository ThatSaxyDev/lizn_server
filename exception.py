from fastapi import Request
from fastapi.responses import JSONResponse

class CustomHTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "failed",
            "statusCode": exc.status_code,
            "message": exc.message
        },
    )