from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework.views import exception_handler
from django.utils.translation import gettext as _
from rest_framework_simplejwt import exceptions


class BaseValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'
    key = 'black_list_validations'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail

        if code is None:
            code = self.default_code

        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    auth_exceptions = (exceptions.InvalidToken, exceptions.AuthenticationFailed,
                       exceptions.TokenBackendError, exceptions.TokenError)

    if response is not None and type(exc) not in auth_exceptions:
        custom_response = {}
        if hasattr(exc, 'key'):
            if exc.key:
                custom_response['key'] = exc.key
        else:
            custom_response['key'] = 'validations'

        custom_response['messages'] = response.data
        response.data = custom_response
        return response

    return response
