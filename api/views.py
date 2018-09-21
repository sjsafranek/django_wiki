from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api(request):
    return HttpResponse("TODO")

def ping(resquest):
    return JsonResponse({"status":"ok", "message": "pong"})
