"""URLs de empleado"""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Vistas
from .views import employee as employee_views

router = DefaultRouter()
router.register(r'employee', employee_views.EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls))
]
