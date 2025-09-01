from django.conf import settings
from apps.store.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = list(self.cart.keys())
        for p in product_ids:
            try:
                self.cart[str(p)]['product'] = Product.objects.get(pk=p)
            except Product.DoesNotExist:
                self.remove(p)
                continue

        for item in self.cart.values():
            item['total_price'] = float(item['price']) * int(item['quantity'])
            yield item

    def has_product(self, product_id):
        if product_id in self.cart:
            return True
        return False
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': product.price, 'id': product_id}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += 1

        # Remove item if quantity <= 0
        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product_id)
        else:
            self.save()


    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_total_length(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_cost(self):
        return sum(float(item['price']) * int(item['quantity']) for item in self.cart.values())
