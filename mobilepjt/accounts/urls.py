from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path


urlpatterns = [
    path('scema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
