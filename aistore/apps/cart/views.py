import json
from django.shortcuts import render
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    
    products = []

    for item in cart:
        product = item['product']
        products.append({
            'id': product.id,
            'title': product.title,
            'price': float(product.price),
            'quantity': item['quantity'],
            'total_price': item['total_price']
        })

    context = {
        'cart': cart,
        'products_json': json.dumps(products)  # Proper JSON array
    }
    return render(request, 'cart.html', context)
