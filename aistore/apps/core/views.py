from django.shortcuts import render
from django.db.models import Q

from apps.store.models import *
# Create your views here.
def frontpage(request):
    products = Product.objects.filter(parent__isnull=True).order_by('-dateadded')
    featured_products = Product.objects.filter(
        parent__isnull=True
    ).filter(
        Q(is_featured=True) | Q(view_count__gt=10)
    ).order_by('-view_count')[:5]
    
    # Get categories with their top 4 products
    categories = Category.objects.all().order_by('ordering')
    category_products = {}
    for category in categories:
        category_products[category.id] = category.products.filter(parent__isnull=True).order_by('-dateadded')[:4]
    
    context = {
        'products': products,
        'featured_products': featured_products,
        'categories': categories,
        'category_products': category_products,
        'active_category': '',  # No category highlighted on frontpage
    }
    return render(request, 'frontpage.html', context)


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')


def featured_products_page(request):
    featured_products = Product.objects.filter(
        parent__isnull=True
    ).filter(
        Q(is_featured=True) | Q(view_count__gt=10)
    ).order_by('-view_count')
    context = {
        'featured_products': featured_products,
        'active_category': '',
    }
    return render(request, 'featured.html', context)

