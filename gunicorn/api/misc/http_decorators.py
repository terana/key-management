import json

from .api_response import APIResponse, APIResponseCodes


def get_dict_from_request(request):
    if request.method == 'GET':
        return request.GET
    elif request.method == 'POST':
        return json.loads(request.body.decode())
    else:
        raise NotImplemented


def require_arguments(required):
    def decorator(func):
        def wrapper(request):
            request_params = get_dict_from_request(request)
            for param in required:
                if param not in request_params:
                    return APIResponse(code=APIResponseCodes.RESPONSE_CODE_BAD_REQUEST,
                                       message=f"Missing argument: {param}")
            return func(request)

        return wrapper

    return decorator
