from django.shortcuts import render

from apps.store.models import *
# Create your views here.
def frontpage(request):
    products = Product.objects.filter(parent__isnull=True).order_by('-dateadded')
    context = {
        'products': products,
        'active_category': '',  # No category highlighted on frontpage
    }
    return render(request, 'frontpage.html', context)


def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

