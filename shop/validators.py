from django.http import JsonResponse
from rest_framework import status


def custom_exception_handler(exc, context):
    if exc.default_code == 'invalid':
        message = 'Validation Error'
        return JsonResponse(
            {"data": {"errorCode": 422, "message": message, "errors": exc.detail}},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif exc.default_code == 'not_authenticated':
        message = 'Login failed'
        return JsonResponse(
            {"error": {"errorcode": 403, "message": message}}, status=status.HTTP_403_FORBIDDEN)

    elif exc.default_code == 'permission_denied':
        message = 'Forbidden for you'
        return JsonResponse(
            {"error": {"code": 403, "message": message}}, status=status.HTTP_403_FORBIDDEN)
