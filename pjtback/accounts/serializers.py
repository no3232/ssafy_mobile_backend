from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.utils.translation import gettext_lazy as _


class CustomRegisterSerializer(RegisterSerializer):
    # 기본 설정 필드: username, password, email
    # 추가 설정 필드: profile_image
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
        user.phone_number = self.data.get('phone_number')
        user.profile_image = self.data.get('profile_image')
        user.naver_email = self.data.get('naver_email')
        user.kakao_email = self.data.get('kakao_email')
        user.google_email = self.data.get('google_email')
        user.save()
        return user
