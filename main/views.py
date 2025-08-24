from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import RegisterForm, CheckoutForm, OrderEditForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
import json

def home(request):
    category = request.GET.get('category')
    search = request.GET.get('search')

    items = FoodItem.objects.all()

    if category:
        items = items.filter(category=category)

    if search:
        items = items.filter(name__icontains=search)

    return render(request, 'main/home.html', {'items': items})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Successfully registered and logged in!")
            return redirect('home')
        else:
            messages.error(request, "Failed to register, Username already exists!")
    else:
        form = RegisterForm() 
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, "Login failed. Please check your Username or Password and Try again.")
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-ordered_at')
    return render(request, 'main/my_orders.html', {'orders': orders})

@login_required
def add_to_cart(request, item_id):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to add items to cart.")
    else:

        item = FoodItem.objects.get(id=item_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Item added to cart!")
    return redirect('home')

@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.get(user=request.user, item_id=item_id).delete()
    return redirect('cart')

@require_POST
def update_quantity_ajax(request):
    data = json.loads(request.body)
    item_id = data.get("item_id")
    quantity = int(data.get("quantity"))

    cart_item = CartItem.objects.get(user=request.user, item_id=item_id)
    cart_item.quantity = quantity
    cart_item.save()

    # Recalculate total
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(ci.item.price * ci.quantity for ci in cart_items)

    return JsonResponse({
        "success": True,
        "new_quantity": cart_item.quantity,
        "total_price": total_price,
    })

@login_required
def cart_drawer(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(i.quantity * i.item.price for i in cart_items)
    return render(request, 'main/cart_drawer.html', {'cart_items': cart_items, 'total': total})

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != 'Pending':
        messages.error(request, "Only pending orders can be edited.")
        return redirect('my_orders')

    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated successfully.")
            return redirect('my_orders')
    else:
        form = OrderEditForm(instance=order)

    return render(request, 'main/edit_order.html', {'form': form, 'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'Pending':
        messages.error(request, "Only pending orders can be cancelled.")
    else:
        order.status = 'Cancelled'
        order.save()
        messages.error(request, "Order has been cancelled.")

    return redirect('my_orders')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    # Get user profile data for initial form values
    profile = None
    try:
        profile = request.user.profile  # Adjust if your profile relation is named differently
    except:
        profile = None

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Create OrderItem entries for each cart item
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    item_name=cart_item.item.name,
                    quantity=cart_item.quantity,
                    price=cart_item.item.price
                )

            cart_items.delete()  # Clear cart after order placed
            messages.success(request, "Order placed successfully!")
            return redirect('order_success')
    else:
        # Pre-fill the form with profile data for GET requests
        initial_data = {}
        if profile:
            # Assuming your CheckoutForm fields match these profile attributes
            initial_data = {
                'full_name': profile.user,
                'phone': profile.phone,
                'email': profile.email,
                'address': profile.address,
            }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'main/checkout.html', {'form': form})


def order_success(request):
    return render(request, 'main/order_success.html')

@staff_member_required
def admin_order_list(request):
    orders = Order.objects.all().order_by('-ordered_at')
    return render(request, 'main/admin_order_list.html', {'orders': orders})


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")
    return redirect('admin_order_list')


@staff_member_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, f"Order #{order.id} deleted.")
    return redirect('admin_order_list')

@login_required
def profile_view(request):
    profile = request.user.profile
    edit_mode = request.GET.get("edit") == "true"

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
        'edit_mode': edit_mode
    }
    return render(request, 'main/profile.html', context)