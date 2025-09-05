# Run this in your terminal to forward Stripe webhooks:
# stripe listen --forward-to localhost:8000/hooks/
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from apps.cart.cart import Cart
from apps.order.utils import checkout as create_order
from apps.order.models import Order,OrderItem
from .models import Product
import json 
import stripe
from django.conf import settings
from apps.coupon.models import Coupon

stripe.api_key = settings.STRIPE_API_KEY_HIDDEN


def create_checkout_session(request):
    try:
        data = json.loads(request.body)
        coupon_code = data['coupon_code']
        coupon_value = 0
        if coupon_code != '':
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.is_valid():
                coupon_value = coupon.discount
                coupon.use()
            
        cart = Cart(request)

        items = []
        for item in cart:
            product = item['product']
            price = int(product.price*100 )  # convert to cents
            if coupon_value > 0:
                discount_amount = int((coupon_value / 100) * price)
                price -= discount_amount
            obj = {
                'price_data': {
                    'currency': 'bdt',
                    'product_data': {
                        'name': product.title,
                    },
                    'unit_amount': price,
                },
                'quantity': item['quantity'],
            }
            items.append(obj)

     
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url='http://127.0.0.1:8000/cart/success/',
            cancel_url='http://127.0.0.1:8000/cart/',
        )

  
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        address = data['address']
        zipcode = data['zipcode']
        place = data['place']

        orderid = create_order(request, first_name, last_name, email, address, zipcode, place)
        order = Order.objects.get(pk=orderid)
        order.payment_intent = session.id
        order.paid = False  

        total_cost = 0
        for item in cart:
            product = item['product']
            price = int(product.price * 100)  # cents
            if coupon_value > 0:
                discount_amount = int((coupon_value / 100) * price)
                price -= discount_amount
            total_cost += price * item['quantity']

        # Stripe expects cents, but your order.paid_amount should be in main currency
        order.paid_amount = total_cost // 100  # convert back to main currency
        order.used_coupon = coupon_code
        order.save()
        return JsonResponse({'id': session.id})
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

def add_to_cart_form(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        cart = Cart(request)
        product = get_object_or_404(Product, pk=product_id)
        cart.add(product=product, quantity=quantity, update_quantity=False)

        # Check if AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            return redirect('cart')

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
