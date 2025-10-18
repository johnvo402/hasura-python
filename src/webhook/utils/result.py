from typing import TypeVar, Generic, Optional, Dict, Any

from ..actions.models import ActionWebhookErrorResponse, ActionExtensionResponse

T = TypeVar('T')

class Result(Generic[T]):
    def __init__(
        self,
        success: bool,
        data: Optional[T] = None,
        error: Optional[str] = None,
        status_code: Optional[int] = 200
    ):
        self.success = success
        self.data = data
        self.error = error
        self.status_code = status_code
        

    @classmethod
    def ok(cls, data: T) -> 'Result[T]':
        """Create a successful result"""
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, message: str, code: int, path: Optional[str] = None, location: Optional[str] = None) -> 'Result[T]':
        """Create a failed result"""
        error_response = ActionWebhookErrorResponse(
            message=message,
            extensions=ActionExtensionResponse(
                path=path,
                location=location
            )
        )
        return cls(success=False, error=error_response.model_dump(), status_code=code)