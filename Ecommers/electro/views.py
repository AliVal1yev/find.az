from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart, CartItem, SubCategory
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    cart.items.add(cart_item)
    cart.save()

    return redirect('home')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart
    }
    return render(request, 'electro/cart.html', context)


def reset_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.clear()
    CartItem.objects.filter(user=request.user).delete()
    cart.save()
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