import os
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import NewUserForm, ProductForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum
from .models import Product, Cart


def home_page(request):
    return render(request, 'home.html', {})


def store_page(request):
    products = Product.objects.all()
    return render(request, 'store.html', {'products':products})


def signup_page(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password )
            messages.success(request, 'You have successfully registered')
            login(request, user)
            return redirect('home')
    else:
        form = NewUserForm()
        return render(request, 'signup.html', {'register_form':form})
    return render(request, 'signup.html', {'register_form':form})


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'home.html',{'user':user})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'login_form':form})
    return render(request, 'login.html', {'login_form':form})


def logout_page(request):
    logout(request)
    messages.success(request, 'You have logged out successfully')
    return redirect('home')


def product_info(request, pi):
    if request.user.is_authenticated:
        product_info = Product.objects.get(id=pi)
        return render(request, 'product_info.html', {'product_info':product_info})
    else:
        messages.success(request, 'You must be logged in to view that page')
        return redirect('home')
    

def add_product(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.added_by = request.user
                product.save()
                messages.success(request, 'You successfully added new item.')
                return redirect('my_items')
        else:
            form = ProductForm()
        return render(request, 'add_product.html', {'add_product_form':form})
    else:
        messages.success(request, 'You must be logged in to view that page.')
        return redirect('home')

    
def delete_product(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        if product.added_by == request.user:
            if request.method == 'POST':
                if product.image:
                    image_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
                    if os.path.exists(image_path):
                        os.remove(image_path)
                product.delete()
                messages.success(request, 'Your product deleted successfully.')
                return redirect('home')
        else:
            messages.error(request, 'You do not have permission to delete this product.')
            return redirect('home')
    else:
        messages.error(request, 'You must be logged in to delete this product.')
        return redirect('home')



def my_items_page(request):
    user_items = Product.objects.filter(added_by=request.user)
    item_count = user_items.count()
    return render(request, 'my_items.html', {'user_items':user_items, 'item_count':item_count})


def cart(request):
    cart, created = Cart.objects.get_or_create(user = request.user)
    total_price = cart.items.aggregate(total=Sum('price'))['total'] or 0
    return render(request, 'cart.html', {'cart':cart, 'total_price':total_price})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user = request.user)
    if product.added_by == request.user:
        messages.success(request, 'You cannot add your item in your cart.')
    elif product in cart.items.all():
        messages.success(request, 'This item is already in your cart.')
    else:
        cart.add_to_cart(product)
        messages.success(request, 'Successfully added item in your cart.')
        return redirect('store')
    return redirect('store')


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user = request.user)
    cart.remove_from_cart(product)
    return redirect('cart')

