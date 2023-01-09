from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.utils.translation import gettext_lazy as _
try:
    from allauth.account import app_settings as allauth_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
    from allauth.utils import email_address_exists, get_username_max_length
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')


class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: profile_image
    phone_number = serializers.CharField(max_length=13)
    profile_image = serializers.ImageField(use_url=True, required=False)
    naver_email = serializers.EmailField(required=False)
    kakao_email = serializers.EmailField(required=False)
    google_email = serializers.EmailField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['profile_image'] = self.validated_data.get('profile_image', '')

        return data




class CustomLoginSerializer(LoginSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: profile_image

    def get_cleaned_data(self):
        data = super().get_cleaned_data()

        return data
