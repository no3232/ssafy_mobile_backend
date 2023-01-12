from django.urls import path
from . import views

urlpatterns = [
    path('outline', views.community_list),
    path('detail/', views.community_detail),
    path('comment/', views.comment_list),
    path('comment/modify', views.comment_detail),
    path('image/', views.community_image),
    path('travel/start', views.traval_start),
    path('travel/pointcollect', views.travel_point_collect),
]