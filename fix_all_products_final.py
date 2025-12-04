#!/usr/bin/env python3
"""
Final fix for all N/A values in product cards
"""

import re
import subprocess

# Get all product info
print("Loading product information...")
products = {}

with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    # Try multiple patterns for Year
    year = ""
    year_patterns = [
        r'<li><span>Year:</span>\s*(\d{4})',
        r'<strong>Year:</strong>\s*(\d{4})',
        r'Year[:\s]+(\d{4})',
        r'Year[:\s]*</span>\s*(\d{4})',
    ]
    for pattern in year_patterns:
        match = re.search(pattern, html, re.I)
        if match:
            year = match.group(1)
            break
    
    # Try multiple patterns for Hours
    hours = ""
    hours_patterns = [
        r'<li><span>(?:Hours|Usage):</span>\s*(\d+)',
        r'<strong>(?:Hours|Usage):</strong>\s*(\d+)',
        r'(?:Hours|Usage)[:\s]+(\d+)',
        r'(?:Hours|Usage)[:\s]*</span>\s*(\d+)',
    ]
    for pattern in hours_patterns:
        match = re.search(pattern, html, re.I)
        if match:
            hours = match.group(1)
            break
    
    products[clean_slug] = {
        'year': year if year else '',
        'hours': hours if hours else ''
    }
    print(f"  {clean_slug}: Year={products[clean_slug]['year']}, Hours={products[clean_slug]['hours']}")

print(f"\nLoaded {len(products)} products\n")

# Fix index.html
print("Fixing index.html...")
with open('index.html', 'r') as f:
    content = f.read()

for slug, info in products.items():
    if info['year'] and info['hours']:
        # Replace N/A for this specific product
        old = f'<span><strong>Year:</strong> N/A</span>\n                                <span><strong>Hours:</strong> N/A</span>\n                            </div>\n                            <a href="product-{slug}.html"'
        new = f'<span><strong>Year:</strong> {info["year"]}</span>\n                                <span><strong>Hours:</strong> {info["hours"]}</span>\n                            </div>\n                            <a href="product-{slug}.html"'
        content = content.replace(old, new)

with open('index.html', 'w') as f:
    f.write(content)
print("✓ index.html fixed\n")

# Fix catalog.html
print("Fixing catalog.html...")
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, info in products.items():
    if info['year']:
        old = f'<span class="spec-label-compact">Year:</span>\n                                    <span class="spec-value-compact">N/A</span>'
        new = f'<span class="spec-label-compact">Year:</span>\n                                    <span class="spec-value-compact">{info["year"]}</span>'
        # Find in context of this product
        pattern = f'product-{re.escape(slug)}\\.html[^>]*>.*?{re.escape(old)}'
        replacement = f'product-{slug}.html" class="btn btn-primary" style="width: 100%; text-align: center;">Details</a>\n                        </div>\n                    </div>\n\n                    <!-- Next product -->\n                    <div class="product-card-compact">\n                        <div class="product-image-compact">\n                            <img src="images/{slug}/main.jpg" alt="{slug}">\n                            <div style="position: absolute; top: 10px; right: 10px; background: var(--primary-color); color: white; padding: 0.3rem 0.8rem; border-radius: 5px; font-weight: 600; font-size: 0.8rem;">Used</div>\n                        </div>\n                        <div class="product-content-compact">\n                            <h3>{slug}</h3>\n                            <p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;">$Price</p>\n                            <p>{slug} - Premium equipment in excellent condition.</p>\n                            <div class="specs-grid-compact">\n                                <div class="spec-item-compact">\n                                    {new}'
        content = content.replace(old, new)
    
    if info['hours']:
        old = f'<span class="spec-label-compact">Hours:</span>\n                                    <span class="spec-value-compact">N/A</span>'
        new = f'<span class="spec-label-compact">Hours:</span>\n                                    <span class="spec-value-compact">{info["hours"]}</span>'
        content = content.replace(old, new)

with open('catalog.html', 'w') as f:
    f.write(content)
print("✓ catalog.html fixed\n")

print("✓ All done!")

