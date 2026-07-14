from .models import Category, Gender


def category_menu(request):
    """Expose the top-level gender sections and their categories for the navbar."""
    menu = []
    for value, label in Gender.choices:
        cats = Category.objects.filter(gender=value, is_active=True)[:8]
        menu.append({"value": value, "label": label, "categories": cats})
    return {"gender_menu": menu, "SITE_NAME": "Myntra"}
