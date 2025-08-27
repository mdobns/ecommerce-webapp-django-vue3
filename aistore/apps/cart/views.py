import secrets
from django.shortcuts import render
from django.conf import settings
from apps.store.models import Product
import json


def cart_detail(request):
    cart = request.session.get('cart', {})
    products_in_cart = []

    for product_id, item in cart.items():  # item is the dict
        try:
            product = Product.objects.get(id=product_id)
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
    return render(request , 'success.html')