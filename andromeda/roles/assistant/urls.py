"""URLs de auxiliares de sistemas."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Vistas
from .views import assistant as assistant_views

router = DefaultRouter()
router.register(r'assistants', assistant_views.AssistantViewSet, basename='assistants')

urlpatterns = [
    path('', include(router.urls))
]
