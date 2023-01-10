from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login

from django.http import JsonResponse

# Create your views here.

# 전화번호 받아와서 중복 검증
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def filtering_phone(request):
    print(request.POST)
    phone = request.POST.get('phone')
    print(phone)
    peoples = get_user_model().objects.filter(phone_number=phone)
    print("------------")
    print(bool(peoples))
    print("------------")
    context = {
        'is_duplicated': bool(peoples)
    }
    return JsonResponse(context)

# 이메일 중복검증
@csrf_exempt
def filtering_email(request):
    print(request.POST)
    email = request.POST.get('email')
    print(email)
    peoples = get_user_model().objects.filter(email=email)
    print("------------")
    print(bool(peoples))
    print("------------")
    context = {
        'is_duplicated': bool(peoples)
    }
    return JsonResponse(context)

# 소셜 로그인 시 유저 정보 조회 후 토큰 발급
# @csrf_exempt
def social_login(request):
    from rest_framework.authtoken.models import Token
    # print(request.POST)
    useremail = request.POST.get('email')
    User = get_user_model()
    try:
        user = get_object_or_404(User, email=useremail)
    except:
        return JsonResponse({"no one": False})
    userid = user.pk
    token = Token.objects.get(user__pk=userid)
    # print("----------------------")
    # print(token)
    # print("----------------------")
    token = get_tokens_for_user(user)
    context = {
        "token": {"refresh": token["refresh"],
                "access": token["access"], },
        "user": {}
    }
    return JsonResponse(context)

# 토큰 생성 함수
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
