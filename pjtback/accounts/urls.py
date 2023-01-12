from django.urls import path, include
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('phonecheck/', views.filtering_phone),
    path('emailcheck/', views.filtering_email),
    path('social_login/', views.social_login),
    path('login2/', views.login2),
    path('detail/<int:userpk>', views.user_detail),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swaggerui'),
]