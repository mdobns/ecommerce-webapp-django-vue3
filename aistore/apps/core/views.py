from django.shortcuts import render

from apps.store.models import *
# Create your views here.
def frontpage(request):
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'frontpage.html', context)

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')