import json
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .cart import Cart
from apps.order.models import Order

# Run this in your terminal to forward Stripe webhooks:
# stripe listen --forward-to localhost:8000/hooks/

@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        print('Checkout session completed:', session.id)
        order = Order.objects.filter(payment_intent=session.id).first()
        if order:
            order.paid = True
            order.save()
            print('Order marked as paid')
        else:
            print('No order to mark as paid')

    return HttpResponse(status=200)