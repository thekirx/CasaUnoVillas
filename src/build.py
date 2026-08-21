#!/usr/bin/env python3
"""Build both outputs from src/template.html.

  public/index.html            deployed to Vercel; photos served from /img/ so the
                               CDN can cache them and the HTML stays ~70KB
  pitch/casa-uno-villas.html   self-contained single file with photos inlined as
                               data URIs, for email, Artifacts and offline viewing

Usage:  python3 src/build.py
"""
import base64, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "src", "template.html")
IMG_DIR = os.path.join(ROOT, "public", "img")
SITE_HTML = os.path.join(ROOT, "public", "index.html")
INLINE_HTML = os.path.join(ROOT, "pitch", "casa-uno-villas.html")

TITLE = "Casa Uno Villas"
DESC = ("Three private-pool villas in Lubao, Pampanga. Book the whole villa direct "
        "and pay less than the same night on Airbnb.")

HEAD_EXTRA = """<meta name="description" content="{desc}">
<meta name="theme-color" content="#1B1512">
<link rel="canonical" href="/">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="/img/hero.jpg">
<meta name="twitter:card" content="summary_large_image">"""


def split_fragment(src):
    """Template is an Artifact fragment: head-ish content, then page markup."""
    end = src.index("</style>") + len("</style>")
    return src[:end], src[end:]


def load_images():
    imgs = {}
    for name in os.listdir(IMG_DIR):
        if name.lower().endswith(".jpg"):
            imgs[os.path.splitext(name)[0]] = os.path.join(IMG_DIR, name)
    return imgs


def substitute(src, resolver):
    missing = []

    def repl(m):
        key = m.group(1)
        if key not in IMAGES:
            missing.append(key)
            return m.group(0)
        return resolver(key)

    out = re.sub(r"\{\{IMG:([a-z0-9\-]+)\}\}", repl, src)
    if missing:
        sys.exit("missing images: %s" % sorted(set(missing)))
    return out


IMAGES = load_images()

with open(TEMPLATE, encoding="utf-8") as fh:
    template = fh.read()
head, body = split_fragment(template)

# --- public/index.html : external images, full HTML document ---
site_head = substitute(head, lambda k: "/img/%s.jpg" % k)
site_body = substitute(body, lambda k: "/img/%s.jpg" % k)
document = (
    "<!doctype html>\n<html lang=\"en\">\n<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
    + HEAD_EXTRA.format(title=TITLE, desc=DESC) + "\n"
    + site_head
    + "\n</head>\n<body>\n" + site_body.strip() + "\n</body>\n</html>\n"
)
os.makedirs(os.path.dirname(SITE_HTML), exist_ok=True)
with open(SITE_HTML, "w", encoding="utf-8") as fh:
    fh.write(document)

# --- pitch/casa-uno-villas.html : inlined, stays an Artifact fragment ---
cache = {}


def data_uri(key):
    if key not in cache:
        with open(IMAGES[key], "rb") as fh:
            cache[key] = "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode()
    return cache[key]


inline = substitute(template, data_uri)
os.makedirs(os.path.dirname(INLINE_HTML), exist_ok=True)
with open(INLINE_HTML, "w", encoding="utf-8") as fh:
    fh.write(inline)

img_bytes = sum(os.path.getsize(p) for p in IMAGES.values())
print("public/index.html           %7.1f KB  (+ %.1f MB of images in public/img/)"
      % (len(document.encode()) / 1e3, img_bytes / 1e6))
print("pitch/casa-uno-villas.html  %7.1f KB  (photos inlined)"
      % (len(inline.encode()) / 1e3))
print("images: %d" % len(IMAGES))
