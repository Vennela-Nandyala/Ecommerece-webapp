from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from myapp.models import Order
from django.db.models import Sum
from .permission import IsAdmin


from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

# -------------------------------
# ✅ Admin API ViewSets
# -------------------------------

class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_deleted = True
        product.save()
        return Response({'status': 'soft-deleted'})


class OrderAdminViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=['put'])
    def status(self, request, pk=None):
        order = self.get_object()
        order.status = request.data.get('status')
        order.save()
        return Response({'status': 'updated'})

    @action(detail=True, methods=['put'])
    def notes(self, request, pk=None):
        order = self.get_object()
        order.admin_notes = request.data.get('notes')
        order.save()
        return Response({'notes': 'added'})


# -------------------------------
# ✅ Frontend Views
# -------------------------------

# Product List View
def product_list(request):
    products = Product.objects.filter(is_deleted=False)
    return render(request, 'myapp/product_list.html', {'products': products})


# Add to Cart View
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f"Added {product.name} to cart.")
    return redirect('product-list')


# View Cart
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'myapp/cart.html', {'cart_items': cart_items, 'total': total})


# Remove from Cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    messages.info(request, "Item removed from cart.")
    return redirect('view-cart')


# Update Quantity in Cart
def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)
        request.session['cart'] = cart
        messages.success(request, "Cart updated.")
    return redirect('view-cart')


# Clear Cart
def clear_cart(request):
    request.session['cart'] = {}
    messages.info(request, "Cart cleared.")
    return redirect('view-cart')


# Checkout View (Placeholder)
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('product-list')
    return render(request, 'myapp/checkout.html')
class AdminTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != 'admin':
            raise serializers.ValidationError("Access denied: not an admin")
        return data

class AdminLoginView(TokenObtainPairView):
    serializer_class = AdminTokenSerializer
class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status="Pending").count(),
            "total_revenue": Order.objects.aggregate(Sum("total"))["total__sum"],
            "total_products": Product.objects.count()
        })
