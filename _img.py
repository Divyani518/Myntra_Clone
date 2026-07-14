import io, random, os, time
from urllib.request import urlopen, Request
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFilter
from products.models import Product, ProductImage, Brand

# Use loremflickr for real fashion photos (downloaded once, cached locally)
LOREM_QUERIES = {
    'default': ['fashion,model'],
    'dress': ['dress,fashion', 'fashion,model'],
    'saree': ['fashion,model', 'dress,fashion'],
    'ethnic': ['fashion,model', 'dress,fashion'],
    'footwear': ['jeans,fashion', 'fashion,model'],
    'shoe': ['jeans,fashion', 'fashion,model'],
    'jean': ['jeans,fashion', 'fashion,model'],
    'jacket': ['jacket,fashion', 'fashion,model'],
    'beauty': ['beauty,cosmetics', 'fashion,model'],
    'lipstick': ['beauty,cosmetics', 'fashion,model'],
    'cream': ['beauty,cosmetics', 'fashion,model'],
    'perfume': ['beauty,cosmetics', 'fashion,model'],
    'kids': ['kids,fashion', 'fashion,model'],
    't-shirt': ['fashion,model', 'jeans,fashion'],
    'shirt': ['fashion,model', 'jacket,fashion'],
    'top': ['fashion,model', 'dress,fashion'],
}

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch(url, timeout=30):
    req = Request(url, headers=HEADERS)
    return urlopen(req, timeout=timeout).read()

def pick_query(p):
    key = (p.category.name + ' ' + p.name).lower()
    for k, v in LOREM_QUERIES.items():
        if k in key:
            return v
    return LOREM_QUERIES['default']

def make_fallback(idx):
    W, H = 1000, 1333
    img = Image.new('RGB', (W, H), (248, 248, 250))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(248 * (1 - t) + 255 * t)
        g = int(248 * (1 - t) + 255 * t)
        b = int(250 * (1 - t) + 255 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([W//2 - 220, H - 280, W//2 + 220, H - 180], fill=(0, 0, 0, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    img = Image.alpha_composite(img.convert('RGBA'), shadow).convert('RGB')
    d = ImageDraw.Draw(img)
    colors = [(255,99,132),(54,162,235),(255,159,64),(75,192,192),(153,102,255),(46,204,113),(231,76,60),(52,152,219)]
    col = colors[idx % len(colors)]
    d.rounded_rectangle([W//2-160, H//2-120, W//2+160, H//2+220], radius=30, fill=col)
    d.rounded_rectangle([W//2-260, H//2-100, W//2-160, H//2+40], radius=24, fill=col)
    d.rounded_rectangle([W//2+160, H//2-100, W//2+260, H//2+40], radius=24, fill=col)
    d.ellipse([W//2-55, H//2-135, W//2+55, H//2-75], fill=(255, 255, 255))
    return img

BRANDS = ["Nike","Puma","Adidas","H&M","Roadster","Wrogn","Allen Solly","Biba","Anouk","HRX","Libas","U.S. Polo","Rare Rabbit","Levi's","ONLY","Flying Machine","Mast & Harbour","Here&Now","Nautica","Tommy Hilfiger","Calvin Klein","United Colors of Benetton"]
brand_objs = {b: Brand.objects.get_or_create(name=b)[0] for b in BRANDS}

downloaded = 0
fallback_used = 0
errors = []

for p in Product.objects.all():
    queries = pick_query(p)
    existing = list(p.images.all())
    needed = max(1, len(existing))
    
    p.brand = brand_objs[BRANDS[hash(p.id) % len(BRANDS)]]
    mrp = random.choice([999, 1299, 1499, 1999, 2499, 2999, 3499, 3999, 4999])
    price = int(round(mrp * random.uniform(0.45, 0.8)))
    if price >= mrp:
        price = int(mrp * 0.6)
    p.mrp = mrp
    p.price = price
    p.save()
    
    for idx in range(needed):
        query = queries[idx % len(queries)]
        url = f'https://loremflickr.com/1000/1333/{query}?random={hash(str(p.id) + str(idx)) % 10000}'
        saved = False
        
        for attempt in range(2):
            try:
                data = fetch(url)
                if len(data) < 10000:
                    if attempt == 0:
                        continue
                    raise ValueError('too small')
                img = Image.open(io.BytesIO(data))
                if img.size[0] < 500 or img.size[1] < 500:
                    if attempt == 0:
                        continue
                    raise ValueError('too small')
                out = io.BytesIO()
                img.convert('RGB').save(out, format='JPEG', quality=92)
                out.seek(0)
                
                if idx < len(existing):
                    pi = existing[idx]
                else:
                    pi = ProductImage(product=p, is_primary=(idx == 0))
                pi.image.save(f'{p.slug}-{idx}.jpg', ContentFile(out.read()), save=True)
                downloaded += 1
                saved = True
                break
            except Exception as e:
                if attempt == 1:
                    errors.append((p.name, query, str(e)[:60]))
        
        if not saved:
            out = io.BytesIO()
            make_fallback(idx).save(out, format='JPEG', quality=92)
            out.seek(0)
            if idx < len(existing):
                pi = existing[idx]
            else:
                pi = ProductImage(product=p, is_primary=(idx == 0))
            pi.image.save(f'{p.slug}-fallback-{idx}.jpg', ContentFile(out.read()), save=True)
            fallback_used += 1

print(f'downloaded: {downloaded}')
print(f'fallback: {fallback_used}')
print(f'errors: {len(errors)}')
for e in errors[:10]:
    print(' ', e)
