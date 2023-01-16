from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiExample, inline_serializer
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
import requests
import json
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers

from .serializers import EmailUniqueCheckSerializer, PhoneUniqueCheckSerializer, CustomUserDetailSerializer, JoinSerializer


@extend_schema(tags=['registration'], request=PhoneUniqueCheckSerializer, responses=bool, summary='폰 넘버 중복 체크')
@api_view(['POST'])
@csrf_exempt
def filtering_phone(request):
    serializer = PhoneUniqueCheckSerializer(data=request.data)
    if serializer.is_valid():
        return HttpResponse(False)
    else:
        return HttpResponse(True)


@extend_schema(tags=['registration'], request=EmailUniqueCheckSerializer, responses=bool, summary='email 중복 체크')
@api_view(['POST'])
@csrf_exempt
def filtering_email(request):
    serializer = EmailUniqueCheckSerializer(data=request.data)
    if serializer.is_valid():
        return HttpResponse(False)
    else:
        return HttpResponse(True)


# 소셜 로그인 시 유저 정보 조회 후 토큰 발급
@extend_schema(tags=['login'], request=inline_serializer(
    name="InlineFormSerializer",
    fields={
        "token": serializers.CharField(),
    },
), responses={"multipart/form-data": {
    "type": "object",
    "properties": {
        "token": {"type": "object", "properties": {"accesstoken": {"type": "string"}, "refreshtoken": {"type": "string"}}},
        "user": {"type": "object"}},
}}, summary='소셜 로그인 및 토큰 발급')
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


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def join_views(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.method == 'GET':
        serializer = JoinSerializer(user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        if request.user == user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
