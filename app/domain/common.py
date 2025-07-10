from typing import Optional
from enum import Enum
from pydantic import BaseModel

class ErrorCode(Enum):
    UNKNOWN = 0
    INVALID_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    BAD_REQUEST = 400
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    SERVICE_UNAVAILABLE = 503
    RATE_LIMIT_EXCEEDED = 429
    TOO_MANY_REQUESTS = 429
    GATEWAY_TIMEOUT = 504

class BaseResponse(BaseModel):
    error: bool = False
    code: Optional[int] = None
    msg: Optional[str] = None
