from django.urls import path, include
from . import views
from dj_rest_auth.views import (
    LoginView, LogoutView
)

urlpatterns = [
    # rest auth url customize
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),

    path('phonecheck/', views.filtering_phone),
    path('emailcheck/', views.filtering_email),
    path('social_login/<str:social_page>/', views.social_login),
    path('login2/', views.login2),
    path('detail/<int:userpk>/', views.user_detail),
    path('auth/', views.auth_test),
]