import io, os
from urllib.request import urlopen, Request
from django.core.files.base import ContentFile

MEDIA = os.path.join("media", "categories")
os.makedirs(MEDIA, exist_ok=True)

# (keyword, lock, name) — mirrors home/views.py CATEGORY_CARDS
CARDS = [
    ("saree,ethnic", 11, "Ethnic Wear"),
    ("casual,fashion", 12, "Casual Wear"),
    ("sport,fashion", 13, "Men's Activewear"),
    ("sport,fashion", 14, "Women's Activewear"),
    ("dress,fashion", 15, "Western Wear"),
    ("sport,fashion", 16, "Sportswear"),
    ("loungewear,fashion", 17, "Loungewear"),
    ("lingerie,fashion", 18, "Innerwear"),
    ("lingerie,fashion", 19, "Lingerie"),
    ("watch,fashion", 20, "Watches"),
    ("grooming,beauty", 21, "Grooming"),
    ("makeup,beauty", 22, "Beauty & Makeup"),
    ("kids,fashion", 23, "Kids Wear"),
    ("shoes,fashion", 24, "Footwear"),
    ("shoes,fashion", 25, "Men's Footwear"),
    ("heels,fashion", 26, "Women's Footwear"),
    ("suit,fashion", 27, "Office Wear"),
    ("handbag,fashion", 28, "Bags & Wallets"),
    ("handbag,fashion", 29, "Handbags"),
    ("jewellery,fashion", 30, "Jewellery"),
    ("headphones,fashion", 31, "Headphones"),
    ("home,decor", 32, "Home Decor"),
    ("sandal,fashion", 33, "Flip Flops"),
    ("casual,fashion", 34, "Casual Styles"),
    ("fashion,model", 35, "Inclusive Styles"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def fetch(url, timeout=30):
    return urlopen(Request(url, headers=HEADERS), timeout=timeout).read()

ok = 0
for kw, lock, name in CARDS:
    path = os.path.join(MEDIA, f"{lock}.jpg")
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        ok += 1
        continue
    done = False
    for attempt in range(5):
        try:
            url = f"https://loremflickr.com/600/800/{kw}?random={lock * 7 + attempt}"
            data = fetch(url)
            if len(data) < 8000:
                continue
            img = __import__("PIL").Image.open(io.BytesIO(data)).convert("RGB")
            out = io.BytesIO()
            img.save(out, format="JPEG", quality=85)
            out.seek(0)
            with open(path, "wb") as f:
                f.write(out.read())
            ok += 1
            done = True
            break
        except Exception:
            continue
    if not done:
        print("FAILED", name, lock)

print("downloaded/exists:", ok, "of", len(CARDS))
