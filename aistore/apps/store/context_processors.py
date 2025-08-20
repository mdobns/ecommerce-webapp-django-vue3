from .models import Category
from apps.cart.cart import Cart

def menu_categories(request):
    categories = Category.objects.all()

    return {"menu_categories":categories}



def cart_count(request):
    cart = Cart(request)
    return {'cart_count': cart.get_total_length()}
