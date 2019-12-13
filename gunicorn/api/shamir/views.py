from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_redis import get_redis_connection

from ..misc.api_response import APIResponse
from ..misc.http_decorators import require_arguments, get_dict_from_request
from ..misc.storage_encryption import StorageEncryption

con = get_redis_connection("default")


@csrf_exempt
@require_arguments(["share_num", "share_val"])
@require_POST
def upload_share(request):
    params = get_dict_from_request(request)

    con.set(f"shamir_share_{params['share_num']}", params["share_val"])
    shares = con.keys("shamir_share_*")

    if len(shares) >= 3:
        enc, _ = StorageEncryption(prime=2 ** 127 - 1, minimum=3, n_shares=5)
        tuple_shares = [(int(k.decode().replace("shamir_share_", "")), int(con.get(k).decode())) for k in shares]

        settings.CRYPTOGRAPHY_KEY = enc.recover_secret(tuple_shares)
        return APIResponse(message="Successfully recovered master key.")

    return APIResponse(message=f"Continuing collecting shares: {len(shares)}/3.")
