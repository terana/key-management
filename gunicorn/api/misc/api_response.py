from django.http import JsonResponse


class APIResponseCodes:
    RESPONSE_CODE_OK = 200
    RESPONSE_CODE_AUTH_ERROR = 401
    RESPONSE_CODE_BAD_REQUEST = 400
    RESPONSE_CODE_KEY_EXIST = 402


class APIResponse(JsonResponse):
    def __init__(self, code=200, message="", response=None, **kwargs):
        data = {
            "code": int(code),
            "message": str(message),
        }

        if response is not None:
            data["response"] = response

        super().__init__(data, safe=False, **kwargs)
