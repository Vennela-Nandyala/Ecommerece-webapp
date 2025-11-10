# from django.urls import path
# from . import views

# urlpatterns = [
#     path('products/', views.product_list, name='product-list'),
#     path('cart/add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
#     path('cart/', views.view_cart, name='view-cart'),
#     path('order/', views.place_order, name='place-order'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.product_list, name='product-list'),
#     path('cart/add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
# ]
from django.urls import path
from . import views
from .views import AdminLoginView
from myapp.views import AdminDashboardView
urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('cart/', views.view_cart, name='view-cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('api/admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('api/admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
]
# from django.urls import path
# from rest_framework.routers import DefaultRouter
# from .views import ProductAdminViewSet, OrderAdminViewSet

# router = DefaultRouter()
# router.register(r'products', ProductAdminViewSet, basename='admin-products')
# router.register(r'orders', OrderAdminViewSet, basename='admin-orders')

# urlpatterns = router.urls