from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart, CartItem
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required



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