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
        state_get = data.get("state")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        if user_get is None:
            user = UserInformation.objects.create(user_id=user_id_get, username=username_get, first_name=first_name_get,
                                                  last_name=last_name_get, state=state_get)
            user.save()
            return JsonResponse({"user": "set"})
        else:
            user_get.state = state_get
            user_get.start = "شروع کرده"
            user_get.save()
            return JsonResponse({"state": "reset"})


@csrf_exempt
def set_user_start(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id_get = data.get("user_id", "")
        user_start = data.get("start", "")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        user_get.start = user_start
        user_get.save()
        return JsonResponse({"start": "set"})


@csrf_exempt
def set_user_rate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id_get = data.get("user_id", "")
        user_rate = data.get("rate", "")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        if user_get is None:
            return JsonResponse({"user": "not_found"})
        else:
            user_get.rate = user_rate
            user_get.save()
            return JsonResponse({"rate": "set"})


@csrf_exempt
def set_phone_state(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id_get = data.get("user_id", "")
        user_phone_state = data.get("phone_state", "")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        if user_get is None:
            return JsonResponse({"user": "not_found"})
        else:
            user_get.phone_state = user_phone_state
            user_get.save()
            return JsonResponse({"phone_state": "set"})


@csrf_exempt
def set_phone_number(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id_get = data.get("user_id", "")
        user_phone_number = data.get("phone_number", "")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        user_get.phone_number = user_phone_number
        user_get.save()
        return JsonResponse({"phone_number": "set"})


@csrf_exempt
def set_user_state(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id_get = data.get("user_id", "")
        user_state = data.get("state", "")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        if user_get is None:
            return JsonResponse({"user": "not_found"})
        else:
            user_get.state = user_state
            user_get.save()
            return JsonResponse({"state": "set"})


@csrf_exempt
def get_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id_get = data.get("user_id", "")
        user_get = UserInformation.objects.filter(user_id=user_id_get).first()
        get_user_rate = user_get.rate
        get_user_state = user_get.state
        get_phone_state = user_get.phone_state
        get_start = user_get.start
        if user_get is None:
            return JsonResponse({"user": "not found"})
        else:
            return JsonResponse(
                {"user_rate": get_user_rate, "user_state": get_user_state, "phone_state": get_phone_state,
                 "start": get_start})
