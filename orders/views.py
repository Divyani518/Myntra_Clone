from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import random
import string

from .models import Order, OrderItem
from cart.utils import get_or_create_cart
from cart.models import CartItem
from accounts.models import Profile


def generate_order_number():
    return "SC" + "".join(random.choices(string.digits, k=10))


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    items = list(cart.items)
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart:detail")

    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        full_name = request.POST.get("full_name") or request.user.get_full_name() or request.user.username
        order = Order.objects.create(
            user=request.user,
            order_number=generate_order_number(),
            full_name=full_name,
            phone=request.POST.get("phone", profile.phone),
            address_line1=request.POST.get("address_line1", profile.address_line1),
            address_line2=request.POST.get("address_line2", profile.address_line2),
            city=request.POST.get("city", profile.city),
            state=request.POST.get("state", profile.state),
            pincode=request.POST.get("pincode", profile.pincode),
            payment_method=request.POST.get("payment_method", "cod"),
            total=cart.total,
            status="confirmed",
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                name=item.product.name,
                size=item.size,
                quantity=item.quantity,
                price=item.product.price,
            )
        CartItem.objects.filter(cart=cart).delete()
        messages.success(request, f"Order {order.order_number} placed successfully!")
        return redirect("orders:success", order_number=order.order_number)

    context = {
        "cart": cart,
        "items": items,
        "profile": profile,
        "title": "Checkout",
    }
    return render(request, "orders/checkout.html", context)


@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/success.html", {"order": order, "title": "Order Confirmed"})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/list.html", {"orders": orders, "title": "My Orders"})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/detail.html", {"order": order, "title": f"Order {order.order_number}"})
