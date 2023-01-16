from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.utils.translation import gettext_lazy as _
# 회원가입 시리얼라이저
from django.conf import settings

from rest_framework import serializers
from dj_rest_auth.models import TokenModel
from dj_rest_auth.utils import import_callable
from dj_rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer

from allauth.account.adapter import get_adapter
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.utils import setup_user_email

from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from .models import User


class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: phone_number, profile_image, naver_email, kakao_email, google_email
    # 비밀번호 해제
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    # 해제 후 password 하나로 만듦
    password = serializers.CharField(write_only=True, source="password1")
    phone_number = serializers.CharField(max_length=13, required=False)
    profile_image = serializers.ImageField(use_url=True, required=False)
    naver_email = serializers.EmailField(required=False)
    kakao_email = serializers.EmailField(required=False)
    google_email = serializers.EmailField(required=False)
    nickname = serializers.CharField(min_length = 1, required= True)
    age = serializers.IntegerField(required = False)

    # password1, password2, 검증 해제
    def validate(self, data):
        return data

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['profileImg'] = self.validated_data.get('profileImg', '')
        data['phone_number'] = self.validated_data.get('phone_number','')
        data['naver'] = self.validated_data.get('naver','')
        data['google'] = self.validated_data.get('google','')
        data['kakao'] = self.validated_data.get('kakao','')
        data['nickname'] = self.validated_data.get('nickname','Ghost')
        data['age'] = self.validated_data.get('age')

        return data
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )
        user = adapter.save_user(request, user, self, commit=False)
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

class JoinSerializer(serializers.ModelSerializer):
    pw = serializers.CharField(source="password")
    name = serializers.CharField(source="username")
    class Meta:
        model = User
        fields = ('email', 'pw', 'name', 'nickname', 'profileImg', 'age', 'kakao', 'naver', 'google')

# 유저 디테일 시리얼라이저
class CustomUserDetailSerializer(UserDetailsSerializer):
    pw = serializers.CharField(source="password")
    name = serializers.CharField(source="username")
    class Meta(UserDetailsSerializer.Meta):
        fields = ('email', 'pw', 'name', 'nickname', 'profileImg', 'age', 'kakao', 'naver', 'google')
        read_only_fields = ('email', 'password',)





class EmailUniqueCheckSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, min_length=3, max_length=30, validators=[UniqueValidator(queryset=get_user_model().objects.all())])

    class Meta:
        model = User
        fields = ('email', )

class PhoneUniqueCheckSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True, min_length=3, max_length=30, validators=[UniqueValidator(queryset=get_user_model().objects.all())])

    class Meta:
        model = User
        fields = ('phone_number', )