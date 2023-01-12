from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.utils.translation import gettext_lazy as _
# 회원가입 시리얼라이저

class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: phone_number, profile_image, naver_email, kakao_email, google_email
    phone_number = serializers.CharField(max_length=13, required=False)
    profile_image = serializers.ImageField(use_url=True, required=False)
    naver_email = serializers.EmailField(required=False)
    kakao_email = serializers.EmailField(required=False)
    google_email = serializers.EmailField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['profile_image'] = self.validated_data.get('profile_image', '')
        data['phone_number'] = self.validated_data.get('phone_number','')
        data['naver_email'] = self.validated_data.get('naver_email','')
        data['google_email'] = self.validated_data.get('google_email','')
        data['kakao_email'] = self.validated_data.get('kakao_email','')

        return data

# 유저 디테일 시리얼라이저
class CustomUserDetailSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = ('email', )


# 토큰 시리얼라이저

from django.conf import settings

from rest_framework import serializers
from dj_rest_auth.models import TokenModel
from dj_rest_auth.utils import import_callable
from dj_rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer

# This is to allow you to override the UserDetailsSerializer at any time.
# If you're sure you won't, you can skip this and use DefaultUserDetailsSerializer directly
rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})
UserDetailsSerializer = import_callable(
    rest_auth_serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer)
)

class CustomTokenSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user', )




# 중복 검사 serializer 이런식으로 할 수도 있고 사실상 django 는 이렇게 짜는 걸 더 권장하는 것 같음
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from .models import User

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