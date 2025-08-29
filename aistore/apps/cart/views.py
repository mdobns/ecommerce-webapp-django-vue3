import secrets
from django.shortcuts import render
from django.conf import settings
from apps.store.models import Product
import json
from .cart import Cart


def cart_detail(request):
    # cart = request.session.get('cart', {})
    cart = Cart(request)
    products_in_cart = []

    for item in cart:  # item is the dict
        try:
            product = Product.objects.get(id=item['id'])
        except Product.DoesNotExist:
            continue

        quantity = item.get('quantity', 0)
        products_in_cart.append({
            'id': product.id,
            'title': product.title,
            'price': float(product.price),
            'quantity': quantity,
            'total_cost': float(product.price) * quantity
        })

    context = {
        'cart': cart,
        'pub_key' : settings.STRIPE_API_KEY_PUBLISHABLE,
        'products_json': json.dumps(products_in_cart)
    }
    return render(request, 'cart.html', context)


def success(request):
    cart = Cart(request)
    cart.clear()
    return render(request , 'success.html')