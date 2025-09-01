from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from django.db.models import Q

def search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'search_results.html', {'products': products, 'query': query})

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {
        "product": product,
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
