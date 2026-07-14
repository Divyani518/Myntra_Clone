from .models import Cart


def get_or_create_cart(request):
    """Return a cart for the current user, supporting anonymous sessions."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def merge_session_cart(request):
    """Move a session cart into the user's cart on login."""
    if not request.user.is_authenticated:
        return
    key = request.session.session_key
    if not key:
        return
    try:
        session_cart = Cart.objects.get(session_key=key)
    except Cart.DoesNotExist:
        return
    user_cart, _ = Cart.objects.get_or_create(user=request.user)
    for item in session_cart.cartitem_set.all():
        existing = user_cart.cartitem_set.filter(product=item.product, size=item.size).first()
        if existing:
            existing.quantity += item.quantity
            existing.save()
        else:
            item.cart = user_cart
            item.save()
    session_cart.delete()
