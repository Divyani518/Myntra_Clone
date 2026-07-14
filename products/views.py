from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest

from .models import Product, Category, Brand, Gender


def _apply_filters(queryset, request):
    gender = request.GET.get("gender")
    category = request.GET.get("category")
    brand = request.GET.getlist("brand")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort", "newest")
    q = request.GET.get("q", "").strip()

    if q:
        queryset = queryset.filter(
            Q(name__icontains=q) | Q(brand__name__icontains=q) | Q(category__name__icontains=q)
        )
    if gender:
        queryset = queryset.filter(gender=gender)
    if category:
        queryset = queryset.filter(category__slug=category)
    if brand:
        queryset = queryset.filter(brand__slug__in=brand)
    if min_price:
        try:
            queryset = queryset.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass

    sort_map = {
        "newest": "-created_at",
        "price-low": "price",
        "price-high": "-price",
        "discount": "-mrp",
        "rating": "-rating",
        "popularity": "-num_ratings",
    }
    queryset = queryset.order_by(sort_map.get(sort, "-created_at"))
    return queryset


def product_list(request):
    products = _apply_filters(Product.objects.select_related("category", "brand"), request)
    paginator = Paginator(products, 24)
    page = paginator.get_page(request.GET.get("page"))
    brands = Brand.objects.all()
    context = {
        "products": page,
        "page_obj": page,
        "brands": brands,
        "title": "All Products",
        "total": products.count(),
    }
    return render(request, "products/list.html", context)


def best_sellers(request):
    qs = Product.objects.select_related("category", "brand")
    products = _apply_filters(qs, request)
    if not request.GET.get("sort"):
        products = products.order_by("-num_ratings", "-rating")
    paginator = Paginator(products, 24)
    page = paginator.get_page(request.GET.get("page"))
    context = {
        "products": page,
        "page_obj": page,
        "brands": Brand.objects.all(),
        "title": "Best Seller Styles",
        "total": products.count(),
        "collection": True,
        "query_url": "?sort=popularity",
        "extra_query": "&sort=popularity",
    }
    return render(request, "products/best_sellers.html", context)


def search(request):
    q = request.GET.get("q", "").strip()
    products = _apply_filters(Product.objects.select_related("category", "brand"), request)
    paginator = Paginator(products, 24)
    page = paginator.get_page(request.GET.get("page"))
    context = {
        "products": page,
        "page_obj": page,
        "query": q,
        "query_url": f"?q={q}" if q else "?",
        "extra_query": f"&q={q}&sort={request.GET.get('sort', 'newest')}",
        "title": f'Search results for "{q}"' if q else "Search",
        "total": products.count(),
    }
    return render(request, "products/search.html", context)


def gender_view(request, gender):
    if gender not in Gender.values:
        return HttpResponseBadRequest("Invalid section")
    categories = Category.objects.filter(gender=gender, is_active=True)
    products = _apply_filters(
        Product.objects.select_related("category", "brand").filter(gender=gender), request
    )
    paginator = Paginator(products, 24)
    page = paginator.get_page(request.GET.get("page"))
    label = dict(Gender.choices).get(gender, gender.title())
    context = {
        "gender": gender,
        "label": label,
        "categories": categories,
        "products": page,
        "page_obj": page,
        "brands": Brand.objects.filter(products__gender=gender).distinct(),
        "title": label,
        "total": products.count(),
        "query_url": f"?gender={gender}",
        "extra_query": f"&gender={gender}&sort={request.GET.get('sort', 'newest')}",
    }
    return render(request, "products/gender.html", context)


def category_view(request, gender, slug):
    category = get_object_or_404(Category, slug=slug, gender=gender, is_active=True)
    products = _apply_filters(
        Product.objects.select_related("category", "brand").filter(category=category), request
    )
    paginator = Paginator(products, 24)
    page = paginator.get_page(request.GET.get("page"))
    context = {
        "category": category,
        "gender": gender,
        "products": page,
        "page_obj": page,
        "brands": Brand.objects.filter(products__category=category).distinct(),
        "title": category.name,
        "total": products.count(),
        "query_url": f"?gender={gender}&category={category.slug}",
        "extra_query": f"&gender={gender}&category={category.slug}&sort={request.GET.get('sort', 'newest')}",
    }
    return render(request, "products/category.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category", "brand").prefetch_related("images"), slug=slug
    )
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
    sizes = ["XS", "S", "M", "L", "XL", "XXL"] if product.gender != "home" else ["Standard"]
    context = {
        "product": product,
        "related": related,
        "sizes": sizes,
        "title": product.name,
    }
    return render(request, "products/detail.html", context)
