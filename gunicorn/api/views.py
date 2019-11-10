from django.http import HttpResponse


def index(request):
    return HttpResponse("terana is the best.")
