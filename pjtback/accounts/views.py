from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse

from rest_framework.decorators import api_view

# Create your views here.

# 전화번호 받아와서 중복 검증
from django.views.decorators.csrf import csrf_exempt


from .serializers import EmailUniqueCheckSerializer
from .serializers import PhoneUniqueCheckSerializer


# 이런 식으로 할 수도 있고.. api_view 에 등록해야 rest_api 로서 등록되는 방식.
# 모델 , serializer , view 함수가 있으면 자동으로 등록 된다고 하는 것 같다. 뭔가 예시로 할만한게 잘 없네. swagger 에서 registration 참고하면 좋을듯
@extend_schema(tags=['테스트'],description='테스트를 위한 메소드입니다')
@api_view(['POST'])
@csrf_exempt
def filtering_phone(request):
    # print(request.POST)
    # phone = request.POST.get('phone')
    # print(phone)
    # peoples = get_user_model().objects.filter(phone_number=phone)
    # print("------------")
    # print(bool(peoples))
    # print("------------")
    # context = {
    #     'is_duplicated': bool(peoples)
    # }
    serializer = PhoneUniqueCheckSerializer(data= request.data)
    if serializer.is_valid():
        context = {
            'is_duplicated': False
        }
    else:
        context = {
            'is_duplicated': True
        }
    return JsonResponse(context)

# 이메일 중복검증
# serializer 쓰도록? 약간 바꿔봤는데 이거는 근데 좀 난이도 있는 블로그 변형 많이 해서 쓰는거라 틀릴 수 있음
# 틀리면 그냥 원상태로 돌리면 될듯 주석처리해놓음
@extend_schema(tags=['테스트'],description='테스트를 위한 메소드입니다')
@api_view(['POST'])
@csrf_exempt
def filtering_email(request):
    # print(request.POST)
    # email = request.POST.get('email')
    # print(email)
    # peoples = get_user_model().objects.filter(email=email)
    # context = {
    #         'is_duplicated': True
    # }

    serializer = EmailUniqueCheckSerializer(data= request.data)
    if serializer.is_valid():
        context = {
            'is_duplicated': False
        }
    else:
        context = {
            'is_duplicated': True
        }
    return JsonResponse(context)

# 소셜 로그인 시 유저 정보 조회 후 토큰 발급
@api_view(['POST'])
@csrf_exempt
def social_login(request):
    # print(request.POST)
    useremail = request.POST.get('email')
    User = get_user_model()
    try:
        user = get_object_or_404(User, email=useremail)
    except:
        return JsonResponse({"no one": False})
    token = get_tokens_for_user(user)
    context = {
        "token": {"refresh": token["refresh"],
                "access": token["access"], },
        "user": user.email
    }
    return JsonResponse(context)

# 토큰 생성 함수
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# 토큰 관련해서 조금 함수구현 끄적이다가 시간도 시간이고 집중 안돼서 일단 놔뒀는데,
# 일단 refresh , access 두개를 쓰려고 하면 그 의의를 찾으려면
# 기본 내장 되어있는 refresh 토큰 가지고 refresh 하는 api 를 만들어야 하고,
# app_setting 부분에 기한 (expired_time 같은?) 거 정해야 할듯 하다. 이 주석은 나중에 구현하면서 지우도록 하자.

@csrf_exempt
def login2 (request):
    useremail = request.POST.get('email')
    password = request.POST.get('password')

    if useremail and password:
        context = {'key': True}
        return JsonResponse(context)
    else:
        context = {'key': False}
        return JsonResponse(context)