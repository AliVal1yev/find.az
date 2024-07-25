from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart, CartItem, SubCategory, Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm, FakePaymentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import stripe
from django.conf import settings
from decimal import Decimal

def home (request):
    categories = Category.objects.all()
    products = Product.objects.order_by('-created_at')
    
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
    print(f"Order: {order}, Created: {created}")

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'price': product.price})
    print(f"OrderItem: {order_item}, Created: {created}")
    
    if not created:
        order_item.quantity += 1
        order_item.price = product.price
    order_item.save()
    print(f"OrderItem after save: {order_item}")
    
    return redirect('home')


@login_required
def view_cart(request):
    orders = Order.objects.filter(customer=request.user, paid=False)
    total = sum(order.get_total_cost() for order in orders)

    # Debugging output
    print(f"Orders for user {request.user.username}: {[order.id for order in orders]}")
    for order in orders:
        print(f"Order ID: {order.id}, Items: {[item.product.name for item in order.items.all()]}")
    
    context = {
        'orders': orders,
        'total': total,
    }
    
    return render(request, 'electro/cart.html', context)


def reset_cart(request):
    # Fetch all unpaid orders for the current user
    orders = Order.objects.filter(customer=request.user, paid=False)
    
    # If you want to set the orders as paid (thus clearing the cart):
    for order in orders:
        order.paid = True
        order.paid_at = timezone.now()
        order.save()
    
    # Alternatively, if you want to delete the unpaid orders entirely:
    # orders.delete()
    
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


stripe.api_key = settings.STRIPE_SECRET_KEY


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