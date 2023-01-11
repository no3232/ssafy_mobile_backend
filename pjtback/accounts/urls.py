from django.urls import path, include
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('phonecheck/', views.filtering_phone),
    path('emailcheck', views.filtering_email),
    path('social_login/', views.social_login),
    path('login2/', views.login2),

    # 필수라네? 이쪽 경로 드가면 yaml 파일 줌 --> 나중에 api 공유를 위한 서버 배포 하게 될 때 필요할지도?
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # option 인데 일단 거의 필수
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swaggerui'),
]