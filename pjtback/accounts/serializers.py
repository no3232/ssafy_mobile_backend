from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
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

        return data
    
    def save(self, request):
        user = super().save(request)
        # 추가 입력 해야할 필드
        user.phone_number = self.data.get('phone_number')
        user.profile_image = self.data.get('profile_image')
        user.naver_email = self.data.get('naver_email')
        user.kakao_email = self.data.get('kakao_email')
        user.google_email = self.data.get('google_email')
        user.save()
        return user


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
