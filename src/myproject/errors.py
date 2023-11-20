from dataclasses import dataclass
from typing import Optional


@dataclass
class ErrorReason(object):
    reason: str
    target: Optional[str]


class BaseError(Exception):
    status: int = 500
    type: str = "myproject_error"
    errors: list[ErrorReason] = []
    headers: dict[str, str] = {}

    def __init__(
        self,
        *args,
        status: int = None,
        type: str = None,
        errors: list[ErrorReason] = None,
        headers: dict[str, str] = None,
    ):
        super().__init__(*args)
        self._set_options(
            status=status,
            type=type,
            errors=errors,
            headers=headers,
        )

    def _set_options(
        self,
        status: int,
        type: str,
        errors: list[ErrorReason],
        headers: dict[str, str],
    ):
        self.status = self.status if status is None else status
        self.type = self.type if type is None else type
        self.errors = self.errors if errors is None else errors
        self.headers = self.headers if headers is None else headers

    def asdict(self) -> dict:
        return {
            'error': {
                'message': ", ".join(self.args),
                'status': self.status,
                'type': self.type,
                'errors': [
                    reason for reason in self.errors
                ],
            },
        }


class NotFoundError(BaseError):
    status: int = 404
    type: str = "not_found_error"


class AuthorizationError(BaseError):
    status: int = 401
    type: str = "authorization_error"


class InvalidJWTError(AuthorizationError):
    type: str = "invalid_jwt_error"


class ExpiredJWTError(AuthorizationError):
    type: str = "expired_jwt_error"


class ExpiredJWTRefreshTokenError(AuthorizationError):
    type: str = "expired_jwt_refresh_token_error"


class LoginAttemptsExceededError(AuthorizationError):
    status: int = 429
    type: str = "login_attempts_exceeded_error"


class UnactivatedAccountError(AuthorizationError):
    type: str = "unactivated_account_error"


class InvalidInputError(BaseError):
    status: int = 400
    type: str = "invalid_input_error"


class RateLimitingError(BaseError):
    status: int = 429
    type: str = "rate_limiting_error"
