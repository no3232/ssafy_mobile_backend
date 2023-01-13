from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiExample
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
import requests
import json

from rest_framework.decorators import api_view

# Create your views here.

# 전화번호 받아와서 중복 검증
from django.views.decorators.csrf import csrf_exempt


from .serializers import EmailUniqueCheckSerializer
from .serializers import PhoneUniqueCheckSerializer


# 이런 식으로 할 수도 있고.. api_view 에 등록해야 rest_api 로서 등록되는 방식.
# 모델 , serializer , view 함수가 있으면 자동으로 등록 된다고 하는 것 같다. 뭔가 예시로 할만한게 잘 없네. swagger 에서 registration 참고하면 좋을듯
@extend_schema(tags=['registration'], parameters=[OpenApiParameter(name="phone_number", required=True, type=str)], summary='폰 넘버 중복 체크')
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
    serializer = PhoneUniqueCheckSerializer(data=request.data)
    if serializer.is_valid():
        return HttpResponse(False)
    else:
        return HttpResponse(True)

# 이메일 중복검증
# serializer 쓰도록? 약간 바꿔봤는데 이거는 근데 좀 난이도 있는 블로그 변형 많이 해서 쓰는거라 틀릴 수 있음
# 틀리면 그냥 원상태로 돌리면 될듯 주석처리해놓음


@extend_schema(tags=['registration'], parameters=[OpenApiParameter(name="email", required=True, type=str)], summary='email 중복 체크')
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

    serializer = EmailUniqueCheckSerializer(data=request.data)
    if serializer.is_valid():
        return HttpResponse(False)
    else:
        return HttpResponse(True)

# 소셜 로그인 시 유저 정보 조회 후 토큰 발급


@extend_schema(tags=['login'], parameters=[OpenApiParameter(name="token", required=True, type=str)], summary='소셜 로그인 및 토큰 발급')
@api_view(['GET', 'POST'])
@csrf_exempt
def social_login(request, social_page):
    # TEST CODE
    # https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=FL_dHs6b8BOH36DPExe3&redirect_uri=http://127.0.0.1:8000/accounts/social_login/1/
    # print(request.GET.get('code'))
    # usercode = request.GET.get('code')
    # userkey = requests.get(url=f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id=FL_dHs6b8BOH36DPExe3&client_secret=p_IuEJYQOc&code={usercode}&state=9kgsGTfH4j7IyAkg', )
    # print(json.loads(userkey.content.decode('utf-8')))
    # usertoken = json.loads(userkey.content.decode('utf-8')).get("access_token")
    # print(usertoken)
    # userdata = requests.get(url="https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"Bearer {usertoken}"})
    # print(json.loads(userdata.content.decode('utf-8')))
    # useremail = json.loads(userdata.content.decode('utf-8')).get('response').get('email')
    # print(useremail)

    # 네이버의 경우
    if social_page == "naver":
        usertoken = request.POST.get("token")
        userdata = requests.get(url="https://openapi.naver.com/v1/nid/me",
                                headers={"Authorization": f"Bearer {usertoken}"})
        print(json.loads(userdata.content.decode('utf-8')))
        useremail = json.loads(userdata.content.decode(
            'utf-8')).get('response').get('email')
    # 카카오의 경우
    elif social_page == "kakao":
        usertoken = request.POST.get("token")
        userdata = requests.get(url="https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {usertoken}"})
    # 구글의 경우
    elif social_page == "google":
        usertoken = request.POST.get("token")
        userdata = requests.get(url="www.googleapis.com/drive/v2/files",
                                headers={"Authorization": f"Bearer {usertoken}"})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # 유저모델 호출
    User = get_user_model()
    try:
        user = get_object_or_404(User, email=useremail)
    except:
        return HttpResponse(False)
    token = get_tokens_for_user(user)
    context = {
        "token": {"refresh": token["refresh"],
                  "access": token["access"], },
        "user": {"email": user.email}
    }
    return JsonResponse(context, status=status.HTTP_200_OK)

# 토큰 생성 함수


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# app_setting 부분에 기한 (expired_time 같은?) 거 정해야 할듯 하다. 이 주석은 나중에 구현하면서 지우도록 하자.

@csrf_exempt
def login2(request):
    useremail = request.POST.get('email')
    password = request.POST.get('password')

    if useremail and password:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@api_view(['DELETE'])
@extend_schema(tags=['registration'], summary='회원가입시 테스트용 delete 작업')
@csrf_exempt
def user_detail(request, userpk):
    user = get_user_model()
    User = get_object_or_404(user, pk=userpk)
    if request.method == 'DELETE':
        User.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_201_CREATED)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def auth_test(request):
    return HttpResponse(True)
