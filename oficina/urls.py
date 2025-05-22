from django.urls import path, include
from rest_framework.routers import DefaultRouter
from oficina.views import ClientViewSet, VehicleViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'vehicle', VehicleViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]