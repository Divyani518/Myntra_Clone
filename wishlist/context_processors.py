from .models import Wishlist, get_wishlist_owner


def wishlist_context(request):
    try:
        owner = get_wishlist_owner(request)
        count = Wishlist.objects.filter(**owner).count()
        product_ids = list(Wishlist.objects.filter(**owner).values_list("product_id", flat=True))
        return {"wishlist_count": count, "wishlist_ids": product_ids}
    except Exception:
        return {"wishlist_count": 0, "wishlist_ids": []}
