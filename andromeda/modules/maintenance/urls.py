"""URLs del modulo de mantenimiento."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Vistas
from .views import maintenance as maintenance_views

router = DefaultRouter()
router.register(r'maintenance', maintenance_views.MaintenanceViewSet, basename='maintenance')

urlpatterns = [
    path('', include(router.urls))
]
