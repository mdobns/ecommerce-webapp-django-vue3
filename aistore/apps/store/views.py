from django.shortcuts import redirect, render,get_object_or_404
from .models import Product,Category, Image
from apps.cart.cart import Cart
from django.db.models import Q
import json

def search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter( Q(title__icontains=query) | Q(description__icontains=query))
    # products = Product.objects.filter(Q(parent__isnull=True) & Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'search_results.html', {'products': products, 'query': query})

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug,)
    
    # Increment view count
    product.view_count += 1
    product.save(update_fields=['view_count'])
    
    cart = Cart(request)
    in_cart = cart.has_product(product.id)
    cart_items = [item['product'].id for item in cart]

    if  product.parent:
        return redirect('product_detail', category_slug=category_slug, slug=product.parent.slug)

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
        "cart_items": cart_items,
    }
    return render(request, 'product_detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(parent__isnull=True).order_by('-dateadded')

    return render(request, "category_detail.html", {
        "category": category,
        "products": products,
        'active_category': slug,
    })
