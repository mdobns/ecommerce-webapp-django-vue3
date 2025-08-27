from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from apps.cart.cart import Cart
from apps.order.utils import checkout as create_order
from apps.order.models import Order,OrderItem
from .models import Product
import json 
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEY_HIDDEN


def create_checkout_session(request):
    cart = Cart(request)

    items = []

    for item in cart:
        product = item['product']
        print(product)
        obj = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.title,
                },
                'unit_amount': int(product.price ),  # convert dollars to cents
            },
            'quantity': item['quantity'],
        }
        items.append(obj)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url='http://127.0.0.1:8000/cart/success/',
            cancel_url='http://127.0.0.1:8000/cart/',
        )
        return JsonResponse({'id': session.id})   # return only session ID
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def checkout(request):
    cart= Cart(request)
    data = json.loads(request.body)
    jsonresponse ={'success': True}

    first_name = data['first_name'] 
    last_name= data['last_name'] 
    email= data['email'] 
    address= data['address'] 
    zipcode= data['zipcode'] 
    place= data['place'] 

    orderid = create_order(request, first_name, last_name, email, address, zipcode, place)

    paid = True

    if paid == True:
        order= Order.objects.get(pk= orderid)
        order.paid = True
        order.paid_amount = cart.get_total_cost()
        order.save()

        cart.clear()
    return JsonResponse({'success': True, 'order_id': orderid})


def api_add_to_cart(request):
    data = json.loads(request.body)
    jsonresponse ={'success': True}
    product_id = data.get('product_id')
    update =data.get('update',False)
    quantity =data.get('quantity',1)

    cart = Cart(request)

    product = get_object_or_404(Product, pk= product_id)

    if not update:
        cart.add(product=product , quantity=1 , update_quantity=False)
    else:
        cart.add(product= product, quantity= quantity, update_quantity=True)

    return JsonResponse(jsonresponse)

def api_remove_from_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = str(data['product_id'])

    cart = Cart(request)
    cart.remove(product_id=product_id)

    return JsonResponse(jsonresponse)
