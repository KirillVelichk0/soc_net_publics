from django.http import HttpResponse


async def index(request):
    return HttpResponse("All ok!")