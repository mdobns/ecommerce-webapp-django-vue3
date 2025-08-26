from apps.cart.cart import Cart

def cart_count(request):
    cart = Cart(request)
    return {'cart_count': cart.get_total_length()}