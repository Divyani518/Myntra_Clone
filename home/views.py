from django.shortcuts import render

from products.models import Product, Category, Brand, Gender
from django.urls import reverse


def index(request):
    featured = Product.objects.filter(is_featured=True).select_related("category", "brand")[:12]
    new_arrivals = Product.objects.all().select_related("category", "brand")[:16]
    top_categories = Category.objects.filter(is_active=True, image__isnull=False).order_by("?")[:8]

    strip = []
    for g in Gender.values:
        c = Category.objects.filter(gender=g, is_active=True, image__isnull=False).first()
        if c:
            strip.append(c)

    rows = []
    for g, label in [("men", "Men"), ("women", "Women"), ("kids", "Kids")]:
        prods = list(Product.objects.filter(gender=g).select_related("category", "brand").order_by("?")[:12])
        if prods:
            rows.append((g, label, prods))

    trending = Product.objects.all().select_related("category", "brand").order_by("-num_ratings", "-rating")[:16]
    top_picks = Product.objects.filter(is_featured=True).select_related("category", "brand")[:12]

    brand_spotlight = Brand.objects.all().order_by("?")[:20]
    featured_brands = Brand.objects.all().order_by("?")[:12]
    luxe_brands = Brand.objects.all().order_by("?")[:8]

    def gurl(g):
        return reverse("products:gender", kwargs={"gender": g})

    slides = [
        {
            "title": "Ethnic Wear",
            "subtitle": "Up to 70% Off",
            "cta": "Shop Now",
            "url": gurl("women"),
            "bg": "https://images.unsplash.com/photo-1613503563564-11c3ec3cce55?w=1400&h=600&fit=crop&q=80&fm=jpg",
            "color": "#fff",
        },
        {
            "title": "Casual Wear",
            "subtitle": "Starting ₹499",
            "cta": "Explore",
            "url": gurl("men"),
            "bg": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=1400&h=600&fit=crop&q=80&fm=jpg",
            "color": "#fff",
        },
        {
            "title": "Sports & Activewear",
            "subtitle": "30–70% Off",
            "cta": "Grab Now",
            "url": gurl("men"),
            "bg": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=1400&h=600&fit=crop&q=80&fm=jpg",
            "color": "#fff",
        },
        {
            "title": "Western Wear",
            "subtitle": "New Arrivals",
            "cta": "Discover",
            "url": gurl("women"),
            "bg": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1400&h=600&fit=crop&q=80&fm=jpg",
            "color": "#fff",
        },
        {
            "title": "Kids Fashion",
            "subtitle": "Up to 60% Off",
            "cta": "Shop Kids",
            "url": gurl("kids"),
            "bg": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=1400&h=600&fit=crop&q=80&fm=jpg",
            "color": "#fff",
        },
        {
            "title": "Beauty & Grooming",
            "subtitle": "Flat 50% Off",
            "cta": "Explore Beauty",
            "url": gurl("beauty"),
            "bg": "https://images.unsplash.com/photo-1522335789203-aabd20f26f69?w=1400&h=600&fit=crop&q=80&fm=jpg",
            "color": "#fff",
        },
    ]

    def cat_url(gender, slug=None):
        if slug:
            try:
                return reverse("products:category", kwargs={"gender": gender, "slug": slug})
            except Exception:
                pass
        return reverse("products:gender", kwargs={"gender": gender})

    # "Shop By Category" — one small promotional card per category (24+ cards)
    CATEGORY_CARDS = [
        {"name": "Ethnic Wear", "discount": "50-80% OFF", "gender": "women", "url": cat_url("women", "ethnic-wear")},
        {"name": "Casual Wear", "discount": "40-80% OFF", "gender": "men", "url": cat_url("men")},
        {"name": "Men's Activewear", "discount": "30-70% OFF", "gender": "men", "url": cat_url("men")},
        {"name": "Women's Activewear", "discount": "30-70% OFF", "gender": "women", "url": cat_url("women")},
        {"name": "Western Wear", "discount": "40-80% OFF", "gender": "women", "url": cat_url("women")},
        {"name": "Sportswear", "discount": "30-80% OFF", "gender": "men", "url": cat_url("men")},
        {"name": "Loungewear", "discount": "30-60% OFF", "gender": "men", "url": cat_url("men")},
        {"name": "Innerwear", "discount": "Up to 70% OFF", "gender": "women", "url": cat_url("women")},
        {"name": "Lingerie", "discount": "Up to 70% OFF", "gender": "women", "url": cat_url("women")},
        {"name": "Watches", "discount": "Up to 80% OFF", "gender": "men", "url": cat_url("men")},
        {"name": "Grooming", "discount": "Up to 60% OFF", "gender": "beauty", "url": cat_url("beauty")},
        {"name": "Beauty & Makeup", "discount": "40-70% OFF", "gender": "beauty", "url": cat_url("beauty")},
        {"name": "Kids Wear", "discount": "Up to 60% OFF", "gender": "kids", "url": cat_url("kids")},
        {"name": "Footwear", "discount": "30-70% OFF", "gender": "men", "url": cat_url("men", "footwear")},
        {"name": "Men's Footwear", "discount": "30-70% OFF", "gender": "men", "url": cat_url("men", "footwear")},
        {"name": "Women's Footwear", "discount": "30-70% OFF", "gender": "women", "url": cat_url("women", "footwear")},
        {"name": "Office Wear", "discount": "40-70% OFF", "gender": "men", "url": cat_url("men")},
        {"name": "Bags & Wallets", "discount": "Up to 70% OFF", "gender": "men", "url": cat_url("men")},
        {"name": "Handbags", "discount": "Up to 70% OFF", "gender": "women", "url": cat_url("women")},
        {"name": "Jewellery", "discount": "Up to 80% OFF", "gender": "women", "url": cat_url("women")},
        {"name": "Headphones", "discount": "Up to 60% OFF", "gender": "men", "url": cat_url("men")},
        {"name": "Home Decor", "discount": "Up to 70% OFF", "gender": "home", "url": cat_url("home")},
        {"name": "Flip Flops", "discount": "Up to 60% OFF", "gender": "men", "url": cat_url("men", "footwear")},
        {"name": "Casual Styles", "discount": "40-80% OFF", "gender": "men", "url": cat_url("men")},
        {"name": "Inclusive Styles", "discount": "Up to 70% OFF", "gender": "women", "url": cat_url("women")},
    ]

    # Reuse locally-stored product images (real fashion photos) so cards always load
    gender_imgs = {}
    for g in ["men", "women", "kids", "beauty", "home"]:
        gender_imgs[g] = [p.primary_image.image.url for p in Product.objects.filter(gender=g) if p.primary_image]
    for c in CATEGORY_CARDS:
        imgs = gender_imgs.get(c["gender"]) or gender_imgs["men"]
        c["img"] = imgs[hash(c["name"]) % len(imgs)] if imgs else ""

    context = {
        "featured": featured,
        "new_arrivals": new_arrivals,
        "top_categories": top_categories,
        "category_strip": strip,
        "category_cards": CATEGORY_CARDS,
        "rows": rows,
        "trending": trending,
        "top_picks": top_picks,
        "brand_spotlight": brand_spotlight,
        "featured_brands": featured_brands,
        "luxe_brands": luxe_brands,
        "slides": slides,
        "title": "Myntra - Online Fashion Shopping",
    }
    return render(request, "home/index.html", context)
