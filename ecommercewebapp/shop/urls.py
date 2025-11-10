from django.urls import path
from .views import shop_home, add_to_cart

urlpatterns = [
    path('', shop_home, name='shop-home'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
]
