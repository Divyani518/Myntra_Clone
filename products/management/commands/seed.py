import os
import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image, ImageDraw, ImageFont

from products.models import Category, Brand, Product, ProductImage, Gender

MEDIA_PRODUCTS = os.path.join("media", "products")

CATEGORY_DATA = {
    "men": ["T-Shirts", "Shirts", "Jeans", "Track Pants", "Sweatshirts", "Footwear"],
    "women": ["Dresses", "Tops", "Ethnic Wear", "Jeans", "Sarees", "Footwear"],
    "kids": ["T-Shirts", "Dresses", "Shorts", "Footwear", "Nightwear"],
    "beauty": ["Lipstick", "Face Cream", "Perfume", "Nail Polish", "Serum"],
    "home": ["Bedsheets", "Cushion Covers", "Curtains", "Wall Decor", "Lamps"],
}

BRANDS = [
    "UrbanVibe", "TrendZ", "StyleNest", "BlueOak", "NovaWear",
    "PureLoom", "CraftHaus", "Lumière", "EarthyTales", "MetroFit",
]

COLORS = ["Black", "Navy Blue", "White", "Olive", "Maroon", "Beige", "Grey", "Mustard"]
FABRICS = ["Cotton", "Rayon", "Polyester", "Linen", "Denim", "Silk Blend", "Modal"]
ADJECTIVES = ["Classic", "Modern", "Casual", "Premium", "Printed", "Solid", "Floral", "Slim Fit", "Relaxed", "Everyday"]


def make_placeholder(width, height, bg, text, sub):
    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    try:
        big = ImageFont.truetype("arial.ttf", 34)
        small = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        big = font
        small = font
    lines = [text[i:i + 18] for i in range(0, len(text), 18)] or [text]
    y = height // 2 - (len(lines) * 22)
    for line in lines:
        draw.text((width // 2 - 90, y), line, fill="white", font=big)
        y += 38
    draw.text((width // 2 - 80, y + 6), sub, fill=(230, 230, 230), font=small)
    return img


class Command(BaseCommand):
    help = "Seed categories, brands and products with generated placeholder images."

    def handle(self, *args, **options):
        os.makedirs(MEDIA_PRODUCTS, exist_ok=True)
        random.seed(42)

        Category.objects.all().delete()
        Brand.objects.all().delete()
        Product.objects.all().delete()

        brand_objs = []
        for b in BRANDS:
            brand_objs.append(Brand.objects.create(name=b, slug=slugify(b)))

        count = 0
        for gender, cats in CATEGORY_DATA.items():
            for cat_name in cats:
                category = Category.objects.create(
                    name=cat_name, gender=gender, is_active=True, sort_order=0
                )
                for i in range(6):
                    name = f"{random.choice(ADJECTIVES)} {cat_name[:-1] if cat_name.endswith('s') else cat_name} {random.choice(['Pro', 'Lite', 'Max', 'Plus', str(i + 1)])}"
                    mrp = Decimal(random.choice([499, 699, 899, 1099, 1299, 1499, 1999, 2499]))
                    discount = random.choice([0, 10, 15, 20, 30, 40, 50])
                    price = round(mrp * (100 - discount) / 100, -2) or mrp
                    product = Product.objects.create(
                        name=name,
                        category=category,
                        brand=random.choice(brand_objs),
                        gender=gender,
                        price=price,
                        mrp=mrp,
                        description=f"A {cat_name.lower()} from our {dict(Gender.choices)[gender]} collection. "
                        f"Crafted with comfort and style in mind, perfect for everyday wear.",
                        fabric=random.choice(FABRICS),
                        color=random.choice(COLORS),
                        rating=round(random.uniform(3.5, 4.9), 1),
                        num_ratings=random.randint(20, 1200),
                        stock=random.randint(0, 50),
                        is_featured=(i < 2),
                    )
                    bg = (
                        random.randint(40, 120),
                        random.randint(40, 120),
                        random.randint(40, 120),
                    )
                    for idx in range(random.randint(1, 3)):
                        ph = make_placeholder(
                            600, 750, bg, product.name[:22], f"{product.brand.name} | {product.color}"
                        )
                        fname = f"{slugify(product.name)}-{idx}.jpg"
                        fpath = os.path.join(MEDIA_PRODUCTS, fname)
                        ph.save(fpath, "JPEG", quality=85)
                        ProductImage.objects.create(
                            product=product,
                            image=os.path.join("products", fname),
                            alt=product.name,
                            is_primary=(idx == 0),
                        )
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {count} products across {Category.objects.count()} categories."))
