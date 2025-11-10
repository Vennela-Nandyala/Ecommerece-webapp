from django.shortcuts import render, redirect
from .models import Product

def shop_home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect('shop-home')

def home_view(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})
