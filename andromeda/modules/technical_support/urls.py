"""URLs de soporte tecnico."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import support as support_views

router = DefaultRouter()
router.register(r'support', support_views.SupportViewSet, basename='support')

urlpatterns = [
    path('', include(router.urls))
]
