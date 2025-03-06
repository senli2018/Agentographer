"""
Standard Response Structure Module

Provides unified API response structure and status code definitions to ensure consistent format for all API returns.
Contains utility functions for success and various error responses to simplify response handling.
"""
from typing import Any, Dict, Optional, Union, Generic, TypeVar
from enum import Enum
from pydantic import BaseModel, Field

# Define generic type variable
T = TypeVar('T')

class ResponseCode(int, Enum):
    """
    Response status code enumeration
    
    HTTP status code style business status codes:
    - 2xxx: Success
    - 4xxx: Client errors
    - 5xxx: Server errors
    
    Business status codes:
    - 1xxxx: Parameter related errors
    - 2xxxx: Business logic errors
    - 3xxxx: Third-party service errors
    - 4xxxx: Database errors
    - 9xxxx: Other errors
    """
    SUCCESS = 200  # Success
    BAD_REQUEST = 400  # Bad request
    UNAUTHORIZED = 401  # Unauthorized
    FORBIDDEN = 403  # Forbidden
    NOT_FOUND = 404  # Resource not found
    METHOD_NOT_ALLOWED = 405  # Method not allowed
    SERVER_ERROR = 500  # Server error
    SERVICE_UNAVAILABLE = 503  # Service unavailable
    GATEWAY_TIMEOUT = 504  # Gateway timeout
    
    # Business status codes
    PARAM_ERROR = 10000  # Parameter error
    BUSINESS_ERROR = 20000  # Business error
    THIRD_PARTY_ERROR = 30000  # Third-party service error
    DATABASE_ERROR = 40000  # Database error
    UNKNOWN_ERROR = 90000  # Unknown error

class ResponseModel(BaseModel, Generic[T]):
    """
    Standard response model
    
    All API responses use this model as a wrapper to ensure uniform format.
    Supports generic data types to accommodate different response data structures.
    """
    code: int = Field(ResponseCode.SUCCESS, description="Business status code")
    message: str = Field("Operation successful", description="Response message")
    data: Optional[T] = Field(None, description="Response data")

def success_response(data: Any = None, message: str = "Operation successful") -> Dict[str, Any]:
    """
    Generate success response
    
    Args:
        data: Response data
        message: Success message
        
    Returns:
        Standard success response dictionary
    """
    return {
        "code": ResponseCode.SUCCESS,
        "message": message,
        "data": data
    }

def error_response(
    code: int = ResponseCode.SERVER_ERROR,
    message: str = "Operation failed",
    data: Any = None
) -> Dict[str, Any]:
    """
    Generate error response
    
    Args:
        code: Error code
        message: Error message
        data: Additional error data
        
    Returns:
        Standard error response dictionary
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }

def param_error(message: str = "Parameter error", data: Any = None) -> Dict[str, Any]:
    """Generate parameter error response"""
    return error_response(
        code=ResponseCode.PARAM_ERROR,
        message=message,
        data=data
    )

def business_error(message: str = "Business processing failed", data: Any = None) -> Dict[str, Any]:
    """Generate business error response"""
    return error_response(
        code=ResponseCode.BUSINESS_ERROR,
        message=message,
        data=data
    )

def third_party_error(message: str = "Third-party service error", data: Any = None) -> Dict[str, Any]:
    """Generate third-party service error response"""
    return error_response(
        code=ResponseCode.THIRD_PARTY_ERROR,
        message=message,
        data=data
    )

def server_error(message: str = "Internal server error", data: Any = None) -> Dict[str, Any]:
    """Generate server error response"""
    return error_response(
        code=ResponseCode.SERVER_ERROR,
        message=message,
        data=data
    ) 