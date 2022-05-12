from django.http import JsonResponse, Http404
from rest_framework import status


def custom_exception_handler(exc, context):
    if type(exc) == Http404:
        return JsonResponse({"error": {"code": 404, "message": "Not found"}},
                            status=status.HTTP_404_NOT_FOUND)
    elif exc.default_code == 'invalid':
        return JsonResponse({"error": {"code": 422, "message": "Validation error", "errors": exc.detail}},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif exc.default_code == 'permission_denied':
        return JsonResponse({"error": {"code": 403, "message": "Forbidden for you"}},
                            status=status.HTTP_403_FORBIDDEN)
