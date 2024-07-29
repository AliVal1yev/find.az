from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart, CartItem, SubCategory, Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm, FakePaymentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import viewsets


def home (request):
    categories = Category.objects.all()
    prod = Product.objects.order_by('-created_at')
    products = []
    
    for product in prod:
        if product.available:
            products.append(product)
            
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'electro/home.html', context)


def deails(request, id):
    prod = Product.objects.get(id=id)
    
    context ={
        'product': prod,
    }
    return render(request, 'electro/details.html', context)



def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'electro/signup.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'electro/login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(customer=request.user, paid=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'price': product.price})
    
    if not created:
        if order_item.quantity >= product.stock:
            return redirect('home')
        order_item.quantity += 1       
        order_item.price = product.price
    order_item.save()
    
    return redirect('home')


@login_required
def view_cart(request):
    orders = Order.objects.filter(customer=request.user, paid=False)
    total = sum(order.get_total_cost() for order in orders)
    
    context = {
        'orders': orders,
        'total': total,
    }
    
    return render(request, 'electro/cart.html', context)


def reset_cart(request):
    orders = Order.objects.filter(customer=request.user, paid=False)

    for order in orders:
        order.paid = True
        order.paid_at = timezone.now()
        order.save()
    
    return redirect('home')


def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__customer=request.user, order__paid=False)
    order = item.order 

    if order.items.count() == 1:
        reset_cart(request)
    else:
        item.delete()
    return redirect('cart')


def subcategory_products(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    products = Product.objects.filter(subcategory=subcategory)
    context = {
        'subcategory': subcategory,
        'products': products
    }
    return render(request, 'electro/subcategory.html', context)


@csrf_exempt
def toggle_favorite(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user in product.favorites.all():
        product.favorites.remove(request.user)
        status = 'removed'
    else:
        product.favorites.add(request.user)
        status = 'added'
    return JsonResponse({'status': status})


@login_required
def wishlist(request):
    user = request.user
    favorite_products = user.favorites_ads.all()

    context ={
        'favorite_products': favorite_products
    }
    return render(request, 'electro/wishlist.html', context)


@login_required
def checkout(request):
    orders = Order.objects.filter(customer=request.user, paid=False)
    total = sum(order.get_total_cost() for order in orders)
    
    if request.method == "POST":
        form = FakePaymentForm(request.POST)
        if form.is_valid():
            for order in orders:
                order.paid = True
                order.paid_at = timezone.now()
                order.save()
                for item in order.items.all():
                    product = get_object_or_404(Product, id=item.product.id)
                    product.stock -= item.quantity
                    # if product.stock == 0:
                    #     product.available = False
                    product.save()
            return redirect('success')
    else:
        form = FakePaymentForm()
    
    context = {
        'orders': orders,
        'total': total,
        'form': form,
    }
    
    return render(request, 'electro/checkout.html', context)


def order_confirmation(request, id):
    order = get_object_or_404(Order, id=id, customer=request.user.customer, paid=True)
    return render(request, 'electro/order_confirmation.html', {'order': order})


def success(request):
    return render(request, 'electro/success.html')


def search_result(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__name__icontains=query) |
            Q(model__name__icontains=query)  
            
        ).distinct()
    else:
        products = Product.objects.all()
    context = {
        'search_term': query,
        'products': products,
    }
    
    return render(request, 'electro/search_result.html', context)




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer