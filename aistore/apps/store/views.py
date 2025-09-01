from django.shortcuts import render,get_object_or_404
from .models import Product,Category, Image
from apps.cart.cart import Cart
from django.db.models import Q
import json

def search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'search_results.html', {'products': products, 'query': query})

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)
    print(f"Product ID: {product.id}")
    in_cart = cart.has_product(product.id)
    

    productstring = [{
        'thumbnail': product.thumbnail.url ,
        'image': product.image.url ,
        
    }]

    for image in product.images.all():
        productstring.append({
        'thumbnail': image.thumbnail.url ,
        'image': image.image.url ,   
        'in_cart': in_cart,
    })

    context = {
        "product": product,
        "productstring": json.dumps(productstring),
        "in_cart": in_cart,
        
    }
    return render(request, 'product_detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()   # thanks to related_name="products"

    return render(request, "category_detail.html", {
        "category": category,
        "products": products,
        'active_category': slug,
    })
