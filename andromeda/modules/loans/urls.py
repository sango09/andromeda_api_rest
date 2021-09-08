"""URLs del modulo de prestamos tecnologicos."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import loans as loans_views
from .views import inventory_loans as inventory_loans_views

router = DefaultRouter()
router.register(r'loans', loans_views.LoansViewSet, basename='loans')
router.register(r'inventory-loans', inventory_loans_views.InventoryLoansViewSet, basename='inventory_loans')

urlpatterns = [
    path('', include(router.urls))
]
