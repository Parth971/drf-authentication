from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if (
        response is not None
        and isinstance(response.data, dict)
        and response.data.get('detail')
    ):
        response.data['message'] = response.data.pop('detail')

    return response
