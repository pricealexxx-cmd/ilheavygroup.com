#!/usr/bin/env python3
"""
Update all product cards in index.html and catalog.html with correct Year and Hours
"""

import re
import subprocess
import os

def extract_product_info(url):
    """Extract Year and Hours from source page"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    # Year
    year = ""
    for pattern in [
        r'<li><span>Year:</span>\s*(\d{4})',
        r'Year[:\s]+(\d{4})',
    ]:
        match = re.search(pattern, html, re.I)
        if match:
            year = match.group(1)
            break
    
    # Hours
    hours = ""
    for pattern in [
        r'<li><span>(?:Hours|Usage):</span>\s*([0-9,]+)',
        r'(?:Hours|Usage)[:\s]+([0-9,]+)',
    ]:
        match = re.search(pattern, html, re.I)
        if match:
            hours = match.group(1).replace(',', '')
            break
    
    return year, hours

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# Build mapping
product_data = {}
for url in urls:
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    year, hours = extract_product_info(url)
    product_data[clean_slug] = (year, hours)

# Update index.html
print("Updating index.html...")
with open('index.html', 'r') as f:
    content = f.read()

for slug, (year, hours) in product_data.items():
    if not year or not hours:
        continue
    
    # Find product card by href
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Year:</strong>\\s*)([^<]+)(</span>.*?<span><strong>Hours:</strong>\\s*)([^<]+)(</span>)'
    
    def replacer(m):
        return m.group(1) + year + m.group(3) + hours + m.group(5)
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)

# Update catalog.html
print("Updating catalog.html...")
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, (year, hours) in product_data.items():
    if not year or not hours:
        continue
    
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Year:</strong>\\s*)([^<]+)(</span>.*?<span><strong>Hours:</strong>\\s*)([^<]+)(</span>)'
    
    def replacer(m):
        return m.group(1) + year + m.group(3) + hours + m.group(5)
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)

print(f"\n✓ Updated {len(product_data)} product cards in index.html and catalog.html")










