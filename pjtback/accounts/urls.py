from django.urls import path, include
from . import views

urlpatterns = [
    path('phonecheck/', views.filtering_phone),
    path('emailcheck/', views.filtering_email),
    path('social_login/', views.social_login),
]