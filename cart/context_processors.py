from .utils import get_or_create_cart


def cart_context(request):
    try:
        cart = get_or_create_cart(request)
        return {
            "cart_count": cart.count,
            "cart_total": cart.total,
        }
    except Exception:
        return {"cart_count": 0, "cart_total": 0}
