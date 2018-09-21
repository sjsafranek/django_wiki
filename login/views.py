from django.http import JsonResponse
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def checkPermissionsHandler(request):
    permissions = Permission.objects.filter(user=request.user)
    user_permissions = []
    for permission in permissions.all():
        user_permissions.append(permission.codename)
    return JsonResponse({
        "status":"ok",
        "data":{
            "permissions": user_permissions
        }
    })
