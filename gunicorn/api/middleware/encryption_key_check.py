from django.conf import settings
import logging

from ..misc.api_response import APIResponse, APIResponseCodes


class EncryptionKeyCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.critical(settings.CRYPTOGRAPHY_KEY)
        if settings.CRYPTOGRAPHY_KEY is None or settings.CRYPTOGRAPHY_KEY == settings.SECRET_KEY:
            if request.path != "/api/shamir/UploadShare":
                return APIResponse(code=APIResponseCodes.RESPONSE_CODE_BAD_REQUEST,
                                   message="Need the secret key to encrypt the database.")

        response = self.get_response(request)
        return response
