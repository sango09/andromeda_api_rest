"""URLs del modulo de inventario tecnologico."""

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import fichaTecnica as ficha_views
from .views import inventory as inventory_views

router = DefaultRouter()
router.register(r'inventory', inventory_views.InventoryViewSet, basename='inventory')
router.register(r'tech-tab', ficha_views.FichaTecnicaViewSet, basename='techtab')

urlpatterns = [
    path('', include(router.urls))
]
