from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import CartItem
from .utils import get_or_create_cart
from products.models import Product


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, "cart/cart.html", {"cart": cart, "title": "Shopping Cart"})


@require_POST
def add_to_cart(request):
    cart = get_or_create_cart(request)
    product_id = request.POST.get("product_id")
    size = request.POST.get("size", "")
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, size=size, defaults={"quantity": quantity}
    )
    if not created:
        item.quantity += quantity
        item.save()
    messages.success(request, f"Added {product.name} to cart.")
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER", "/")
    return redirect(next_url)


@require_POST
def update_cart(request):
    item_id = request.POST.get("item_id")
    qty = request.POST.get("quantity", 1)
    try:
        qty = int(qty)
    except (TypeError, ValueError):
        qty = 1
    item = get_object_or_404(CartItem, id=item_id)
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect("cart:detail")


@require_POST
def remove_from_cart(request):
    item_id = request.POST.get("item_id")
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart:detail")
