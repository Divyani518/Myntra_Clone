from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Wishlist, get_wishlist_owner
from products.models import Product


def wishlist_detail(request):
    owner = get_wishlist_owner(request)
    items = Wishlist.objects.filter(**owner).select_related("product", "product__category")
    return {"wishlist_items": items}


def wishlist_view(request):
    owner = get_wishlist_owner(request)
    items = Wishlist.objects.filter(**owner).select_related("product", "product__category")
    return render(request, "wishlist/wishlist.html", {"items": items, "title": "My Wishlist"})


@require_POST
def add_to_wishlist(request):
    product = get_object_or_404(Product, id=request.POST.get("product_id"))
    owner = get_wishlist_owner(request)
    Wishlist.objects.get_or_create(product=product, **owner)
    messages.success(request, f"Added {product.name} to wishlist.")
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER", "/")
    return redirect(next_url)


@require_POST
def remove_from_wishlist(request):
    product = get_object_or_404(Product, id=request.POST.get("product_id"))
    owner = get_wishlist_owner(request)
    Wishlist.objects.filter(product=product, **owner).delete()
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER", "/")
    return redirect(next_url)
