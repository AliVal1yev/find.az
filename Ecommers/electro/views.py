from django.shortcuts import render
from .models import Product, Category


def home (request):
    categories = Category.objects.all()
    products = Product.objects.order_by('-created_at')
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'electro/home.html', context)


