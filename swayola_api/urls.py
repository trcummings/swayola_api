from django.contrib import admin
from django.urls import path, include
from rest_framework import status
from rest_framework.views import exception_handler, Response
from rest_framework.exceptions import AuthenticationFailed
from http import HTTPStatus
from typing import Any

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('polls.urls'))
]

def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # For all structured exceptions, pass in the status code
    if response is not None:
        status_code = response.status_code
    # Otherwise default to 500
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # Handle authentication failure
    if isinstance(exc, AuthenticationFailed):
        response.data = {
            "message": "Authentication failed. Please check your credentials and try again.",
        }

    elif response is not None:
        # Using the description's of the HTTPStatus class as error message.
        http_code_to_message = { v.value: v.description for v in HTTPStatus }
        # Pass along the error in the response data
        response.data = {
            "message": http_code_to_message[status_code],
            "errors": response.data
        }

    return response