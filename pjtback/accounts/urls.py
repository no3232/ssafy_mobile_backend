from django.urls import path, include
from . import views

urlpatterns = [
    # rest auth url customize
    

    path('phonecheck/', views.filtering_phone),
    path('emailcheck/', views.filtering_email),
    path('social_login/<str:social_page>/', views.social_login),
    path('login2/', views.login2),
    path('detail/<int:userpk>/', views.user_detail),
    path('auth/', views.auth_test),
]