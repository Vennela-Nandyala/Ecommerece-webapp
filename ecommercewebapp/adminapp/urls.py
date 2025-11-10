from django.urls import path
from .views import test_view, ProductListView

urlpatterns = [
    path('test/', test_view),
    path('products/', ProductListView.as_view(), name='admin-product-list'),
]