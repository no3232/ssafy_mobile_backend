from django.urls import path
from . import views

urlpatterns = [

    path('board/', views.board_get),
    path('board/create/', views.board_create),
    # path('outline', views.community_list),
    # path('filtered',views.community_filtered_list),
    # path('create',views.community_create),
    # path('detail/', views.community_detail),
    # path('<int:communtiy_pk>/comment/', views.comment_list),
    # path('<int:communtiy_pk>/comment/create', views.comment_create),
    # path('comment/modify', views.comment_detail),
    # path('image/', views.community_image),
    # path('<int:community_pk>/travel',views.travelpath ),
    # path('<int:community_pk>/travel/start', views.traval_start),
    # path('<int:community_pk>/travel/pointcollect', views.travel_point_collect),
]