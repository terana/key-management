import logging

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from ..misc.api_response import APIResponse, APIResponseCodes
from ..misc.http_decorators import require_arguments, get_dict_from_request
from ..models import Secret, AccessLog


@require_arguments(["key"])
@require_GET
def get_secret(request):
    key = request.GET['key']
    try:
        secret = Secret.objects.get(key=key)
        log = AccessLog(requested_secret=key, result=secret.value)
        log.save()
        return APIResponse(code=APIResponseCodes.RESPONSE_CODE_OK,
                           response={"key": secret.key,
                                     "value": secret.value})
    except ObjectDoesNotExist:
        log = AccessLog(requested_secret=key, exception=True)
        log.save()
        return APIResponse(code=APIResponseCodes.RESPONSE_CODE_AUTH_ERROR,
                           message="Authentication error.")


@csrf_exempt
@require_arguments(["key", "value"])
@require_POST
@login_required
def create_secret(request):
    params = get_dict_from_request(request)
    num_results = Secret.objects.filter(key=params['key']).count()
    if num_results == 0:
        logging.critical("Saving secret")
        secret = Secret.objects.create(key=params['key'], value=params['value'])
        secret.save()

    else:
        return JsonResponse({"msg": "Key already exists in database",
                             "code": APIResponseCodes.RESPONSE_CODE_KEY_EXIST})

    return JsonResponse({"msg": "Successfully created",
                         "code": APIResponseCodes.RESPONSE_CODE_OK})


@require_GET
@login_required
def get_logs(request):
    log = AccessLog(requested_secret="access_logs", result="True")
    log.save()
    obj = AccessLog.objects.all()
    serialized_obj = serializers.serialize('json', obj)
    return APIResponse(response=serialized_obj, code=APIResponseCodes.RESPONSE_CODE_OK)
