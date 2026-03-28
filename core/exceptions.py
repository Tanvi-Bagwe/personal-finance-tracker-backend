# Custom exception handler
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Handle exceptions and format error response"""
    response = exception_handler(exc, context)

    if response is not None:
        raw_error = response.data
        msg = "An error occurred"

        # Extract error message from different response formats
        if isinstance(raw_error, dict):
            first_val = next(iter(raw_error.values()))
            msg = first_val[0] if isinstance(first_val, list) else first_val
        elif isinstance(raw_error, list):
            msg = raw_error[0]

        # Format response consistently
        response.data = {
            "isSuccess": False,
            "message": str(msg),
            "data": None
        }

    return response