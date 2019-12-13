from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core import serializers


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
        return APIResponse(response={"msg": secret.value,
                                     "code": APIResponseCodes.RESPONSE_CODE_OK})
    except ObjectDoesNotExist:
        log = AccessLog(requested_secret=key, exception=True)
        log.save()
        return APIResponse(response={"msg": key,
                                     "code": APIResponseCodes.RESPONSE_CODE_AUTH_ERROR})


@csrf_exempt
@require_arguments(["key", "value"])
@require_POST
@login_required
def create_secret(request):
    params = get_dict_from_request(request)
    # TODO check if key already exists.
    num_results = Secret.objects.filter(key=params['key']).count()

    if num_results == 0:
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
    key = request.GET['key']
    log = AccessLog(requested_secret=key, result="True")
    log.save()
    obj = AccessLog.objects.filter()
    serialized_obj = serializers.serialize('json', [obj, ])
    return JsonResponse({"msg": serialized_obj, "code": APIResponseCodes.RESPONSE_CODE_OK})
