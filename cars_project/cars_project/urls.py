from django.conf import settings 
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
# from cars_app.views import CarViewSet

# router = routers.SimpleRouter()
# router.register(r'cars', CarViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cars_app.urls')),
    # path('api/v1/', include(router.urls)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)