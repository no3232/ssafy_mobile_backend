"""pjtback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls import url
from rest_framework import permissions

from dj_rest_auth.registration.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # 이런 라이브러리 안 쪽에거는 decorator 달아봤는데도 잘 안되더라
    # 잘 모르겠어서 그냥 좀 특이하게 아예 path 네이밍을 바꿨다. 맘에 안들면 원래대로 ㄱㄱ
    path('accounts/rest', include('dj_rest_auth.urls')),
    path('registration/', RegisterView.as_view() , name = 'registration'),
    path('accounts/', include('accounts.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
