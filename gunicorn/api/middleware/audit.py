from gunicorn.api.models import AccessLog


class AuditMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        log = AccessLog(requested_secret=response.key, result=response.value)
        log.save()

        return response
