from django.urls import path
from . import views


urlpatterns = [
    path('phonecheck/', views.filtering_phone),
    path('emailcheck/', views.filtering_email),
    path('social_login/<str:social_page>/', views.social_login),
]