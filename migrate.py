#!/usr/bin/env python3
"""
WordPress → Astro Migration Script v2
Keeps HTML content (no markdown conversion loss)
Validates all downloaded images
Extracts Yoast SEO metadata
"""

import requests, os, re, json, time
from pathlib import Path
from urllib.parse import urlparse

BASE_URL = "https://journeystorm.com"
API_BASE = f"{BASE_URL}/wp-json/wp/v2"
PROJECT = Path("/Users/wong/Desktop/Astroweb/journeystorm")
CONTENT_DIR = PROJECT / "src/content/articles"
IMAGES_DIR = PROJECT / "public/images"

CONTENT_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

downloaded = {}
stats = {"posts": 0, "images": 0, "failed": 0, "pages": 0}


def fetch_paginated(endpoint, per_page=50):
    """Fetch all items from a paginated endpoint."""
    items = []
    page = 1
    while True:
        url = f"{API_BASE}/{endpoint}?per_page={per_page}&page={page}"
        resp = requests.get(url)
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        items.extend(data)
        page += 1
        time.sleep(0.2)
    return items


def download_image(img_url):
    """Download and validate an image. Returns local path or None if invalid."""
    global stats

    img_url = img_url.replace('http://', 'https://')
    if img_url in downloaded:
        return downloaded[img_url]

    parsed = urlparse(img_url)
    filename = os.path.basename(parsed.path.split('?')[0])
    if not filename or '.' not in filename:
        downloaded[img_url] = img_url
        return img_url

    local_path = IMAGES_DIR / filename
    if local_path.exists():
        # Verify existing file is a real image
        with open(local_path, 'rb') as f:
            header = f.read(8)
        if header[:2] == b'\xff\xd8' or header[:4] == b'\x89PN' or header[:4] == b'RIFF' or header[:4] == b'<svg' or header[:6] in (b'GIF89a', b'GIF87a'):
            downloaded[img_url] = f"/images/{filename}"
            return downloaded[img_url]
        else:
            local_path.unlink()  # Delete corrupt file

    try:
        resp = requests.get(img_url, timeout=20)
        if resp.status_code == 200 and len(resp.content) > 500:
            # Validate it's an actual image
            header = resp.content[:8]
            is_image = (header[:2] == b'\xff\xd8' or header[:4] == b'\x89PN' or
                       header[:4] == b'RIFF' or header[:6] in (b'GIF89a', b'GIF87a'))
            if not is_image:
                stats["failed"] += 1
                downloaded[img_url] = None
                return None

            local_path.write_bytes(resp.content)
            stats["images"] += 1
            if stats["images"] % 30 == 0:
                print(f"    Downloaded {stats['images']} images...")
            downloaded[img_url] = f"/images/{filename}"
            return downloaded[img_url]
        else:
            stats["failed"] += 1
            downloaded[img_url] = None
            return None
    except:
        stats["failed"] += 1
        downloaded[img_url] = None
        return None


def process_images_in_html(html):
    """Replace image URLs in HTML with local paths."""
    img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
    img_count = 0

    def replacer(match):
        nonlocal img_count
        old_url = match.group(1).replace('http://', 'https://')
        if 'journeystorm.com' in old_url:
            new_url = download_image(old_url)
            if new_url:
                img_count += 1
                return match.group(0).replace(match.group(1), new_url)
            else:
                # Remove broken images
                return ''
        return match.group(0).replace(match.group(1), old_url)

    result = img_pattern.sub(replacer, html)
    return result


def get_yoast_meta(post_id):
    """Try to get Yoast SEO metadata."""
    try:
        # Yoast stores meta in post meta
        url = f"{API_BASE.replace('wp/v2', 'yoast/v1')}/get_head?post_id={post_id}&url={BASE_URL}/?p={post_id}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Extract meta description from head HTML
            head = data.get('html', '')
            desc_m = re.search(r'<meta name="description" content="([^"]*)"', head)
            title_m = re.search(r'<meta property="og:title" content="([^"]*)"', head)
            og_img_m = re.search(r'<meta property="og:image" content="([^"]*)"', head)
            return {
                'meta_desc': desc_m.group(1) if desc_m else None,
                'og_title': title_m.group(1) if title_m else None,
                'og_image': og_img_m.group(1) if og_img_m else None,
            }
    except:
        pass
    return None


def save_post(post, categories_map):
    """Save a post as an .md file with HTML content."""
    title = post['title']['rendered']
    # Decode entities
    title = re.sub(r'&#8217;', "'", title)
    title = re.sub(r'&#8211;', '–', title)
    title = re.sub(r'&#038;', '&', title)

    slug = post['slug']
    date = post['date'][:10]
    excerpt_html = post['excerpt']['rendered']
    excerpt = re.sub(r'<[^>]+>', '', excerpt_html).replace('[&hellip;]', '...').strip()

    # Categories
    cat_ids = post.get('categories', [])
    cat_names = [categories_map.get(cid, {}).get('name', 'Uncategorized') for cid in cat_ids]
    cat_slugs = [categories_map.get(cid, {}).get('slug', 'uncategorized') for cid in cat_ids]

    # Featured image
    featured_img = None
    if '_embedded' in post and 'wp:featuredmedia' in post['_embedded']:
        fm = post['_embedded']['wp:featuredmedia']
        if fm and len(fm) > 0:
            featured_img = download_image(fm[0]['source_url'])

    # Process content HTML — download and replace images
    content_html = post['content']['rendered']
    content_html = process_images_in_html(content_html)

    # Yoast SEO
    yoast = get_yoast_meta(post['id'])
    meta_desc = yoast['meta_desc'] if yoast else excerpt

    # Clean up HTML artifacts
    content_html = content_html.replace('&#8217;', "'")
    content_html = content_html.replace('&#8211;', '–')
    content_html = content_html.replace('&#038;', '&')

    # Build frontmatter
    fm = "---\n"
    fm += f"title: \"{title}\"\n"
    fm += f"date: \"{date}\"\n"
    fm += f"postSlug: \"{slug}\"\n"
    fm += f"categories: {json.dumps(cat_names, ensure_ascii=False)}\n"
    fm += f"categorySlugs: {json.dumps(cat_slugs, ensure_ascii=False)}\n"
    if meta_desc:
        fm += f"excerpt: \"{meta_desc}\"\n"
    if featured_img:
        fm += f"image: \"{featured_img}\"\n"
    fm += f"urlPath: \"/{slug}/\"\n"
    fm += "---\n\n"
    fm += content_html

    filepath = CONTENT_DIR / f"{slug}.md"
    filepath.write_text(fm)
    stats["posts"] += 1


def main():
    print("=" * 60)
    print("journeystorm.com → Astro Migration v2")
    print("=" * 60)

    # 1. Categories
    print("\n📂 Fetching categories...")
    cats = requests.get(f"{API_BASE}/categories?per_page=30").json()
    cat_map = {c['id']: {'name': c['name'], 'slug': c['slug']} for c in cats}
    for c in cats:
        print(f"  [{c['id']}] {c['name']} ({c['slug']}) — {c['count']} posts")

    with open(CONTENT_DIR.parent / "categories.json", 'w') as f:
        json.dump([{k: v for k, v in c.items() if k in ['id','name','slug','count']} for c in cats], f, ensure_ascii=False, indent=2)

    # 2. Posts
    print("\n📝 Fetching posts...")
    posts = fetch_paginated("posts?_embed=1")
    print(f"  Total: {len(posts)} posts")

    print("\n🔄 Processing posts...")
    for i, post in enumerate(posts):
        save_post(post, cat_map)
        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{len(posts)} posts")

    # 3. Pages
    print("\n📄 Fetching pages...")
    pages = fetch_paginated("pages?_embed=1")
    for p in pages:
        slug = p['slug']
        # Skip theme demo pages
        if slug in ['sample-page']:
            continue
        if any(x in slug for x in ['portfolio', 'columns', 'masonry', 'grid', 'layout']):
            continue
        save_post(p, cat_map)
        stats["pages"] += 1
        print(f"  Saved page: {slug} — \"{p['title']['rendered']}\"")

    # Summary
    print("\n" + "=" * 60)
    print("MIGRATION COMPLETE")
    print("=" * 60)
    print(f"  Posts:       {stats['posts']}")
    print(f"  Images:      {stats['images']} downloaded")
    print(f"  Failed imgs: {stats['failed']}")
    print(f"  Total files: {len(os.listdir(CONTENT_DIR))}")

    # Verify images
    corrupt_count = 0
    for fname in os.listdir(IMAGES_DIR):
        fpath = IMAGES_DIR / fname
        with open(fpath, 'rb') as f:
            h = f.read(8)
        if not (h[:2] == b'\xff\xd8' or h[:4] == b'\x89PN' or h[:4] == b'RIFF' or h[:6] in (b'GIF89a', b'GIF87a')):
            corrupt_count += 1
            fpath.unlink()
    if corrupt_count:
        print(f"  CORRUPT REMOVED: {corrupt_count}")

    print("=" * 60)


if __name__ == "__main__":
    main()
