#!/usr/bin/env python3
"""
Check which products are missing from index.html
"""

import re

# Read all product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# Extract slugs from URLs
product_slugs = []
for url in urls:
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    # Special case
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    product_slugs.append(clean_slug)

# Read index.html
with open('index.html', 'r') as f:
    index_content = f.read()

# Find all product links in index.html
found_products = re.findall(r'href="product-([^"]+\.html)"', index_content)
found_slugs = [slug.replace('.html', '') for slug in found_products]

# Compare
missing = []
for slug in product_slugs:
    if slug not in found_slugs:
        missing.append(slug)

print(f"Всего товаров в списке: {len(product_slugs)}")
print(f"Товаров на главной странице: {len(found_slugs)}")
print(f"Отсутствующих товаров: {len(missing)}")
print()

if missing:
    print("Отсутствующие товары:")
    for i, slug in enumerate(missing, 1):
        # Find original URL
        for url in urls:
            if slug in url.lower() or ('caterpillar-299d3' in slug and '299d3' in url.lower()):
                print(f"{i}. {slug}")
                print(f"   URL: {url}")
                break
else:
    print("✓ Все товары добавлены на главную страницу!")

# Also check for duplicates
from collections import Counter
duplicates = [item for item, count in Counter(found_slugs).items() if count > 1]
if duplicates:
    print(f"\n⚠ Найдены дубликаты на главной странице:")
    for dup in duplicates:
        print(f"  - {dup}")

