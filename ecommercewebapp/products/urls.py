from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminProductViewSet

router = DefaultRouter()
router.register(r'api/admin/products', AdminProductViewSet)

urlpatterns = router.urls