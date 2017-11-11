from __future__ import unicode_literals
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram_backend.models import UserInformation
import json


@csrf_exempt
def set_user_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id_get = data.get("user_id", "")
        username_get = data.get("username", "")
        first_name_get = data.get("first_name", "")
        last_name_get = data.get("last_name", "")
        phone_number = data.get("phone_number", "")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        if user_get is None:
            user = UserInformation.objects.create(user_id=user_id_get, username=username_get, first_name=first_name_get,
                                                  last_name=last_name_get, phone_number=phone_number)
            user.save()
            return JsonResponse({"user": "جدید", "status": "فعال"})
        else:
            return JsonResponse({"user": "وجوددارد", "status": user_get.status})


@csrf_exempt
def set_user_rate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id_get = data.get("user_id", "")
        user_rate = data.get("rate", "")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        user_get.rate = user_rate
        user_get.save()
        return JsonResponse({"rate": "set"})


@csrf_exempt
def check_start(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id_get = data.get("user_id", "")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        if user_get is None:
            return JsonResponse({"start": "شروع نکرده"})
        else:
            return JsonResponse({"start": "شروع کرده"})
