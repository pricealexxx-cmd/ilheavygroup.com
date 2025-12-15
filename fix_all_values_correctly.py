#!/usr/bin/env python3
"""
Correctly fix all Year and Hours values by matching product slugs exactly
"""

import re
import subprocess

# Get product data with correct mapping
products = {}

with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print("Extracting product information...")
for url in urls:
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    # Extract Year
    year = ""
    year_patterns = [
        r'<li><span>Year:</span>\s*(\d{4})',
        r'<strong>Year:</strong>\s*(\d{4})',
        r'Year[:\s]+(\d{4})',
    ]
    for pattern in year_patterns:
        match = re.search(pattern, html, re.I)
        if match:
            year = match.group(1)
            break
    
    # Extract Hours
    hours = ""
    hours_patterns = [
        r'<li><span>(?:Hours|Usage):</span>\s*(\d+)',
        r'<strong>(?:Hours|Usage):</strong>\s*(\d+)',
        r'(?:Hours|Usage)[:\s]+(\d+)',
    ]
    for pattern in hours_patterns:
        match = re.search(pattern, html, re.I)
        if match:
            hours = match.group(1)
            break
    
    products[clean_slug] = {'year': year, 'hours': hours}
    print(f"  {clean_slug}: Year={year}, Hours={hours}")

print(f"\nLoaded {len(products)} products\n")

# Fix index.html - be very specific with product slug matching
print("Fixing index.html...")
with open('index.html', 'r') as f:
    content = f.read()

for slug, info in products.items():
    if not info['year'] or not info['hours']:
        continue
    
    # Very specific pattern - match the exact product card
    # Find: href="product-SLUG.html" ... Year: ... Hours: ...
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<div class="product-specs">.*?<span><strong>Year:</strong>\\s*)([^<]*?)(</span>.*?<span><strong>Hours:</strong>\\s*)([^<]*?)(</span>)'
    
    def replacer(match):
        return match.group(1) + info['year'] + match.group(3) + info['hours'] + match.group(5)
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
print("✓ index.html fixed\n")

# Fix catalog.html
print("Fixing catalog.html...")
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, info in products.items():
    if not info['year'] or not info['hours']:
        continue
    
    # Fix Year
    pattern_year = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Year:</span>\\s*<span class="spec-value-compact">)([^<]*?)(</span>)'
    content = re.sub(pattern_year, lambda m: m.group(1) + info['year'] + m.group(3), content, flags=re.DOTALL)
    
    # Fix Hours
    pattern_hours = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Hours:</span>\\s*<span class="spec-value-compact">)([^<]*?)(</span>)'
    content = re.sub(pattern_hours, lambda m: m.group(1) + info['hours'] + m.group(3), content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)
print("✓ catalog.html fixed\n")

print("✓ All values corrected!")










