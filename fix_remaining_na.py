#!/usr/bin/env python3
"""
Fix remaining N/A values in product cards
"""

import re
import subprocess
import json

def extract_product_info(url):
    """Extract Year and Hours"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    year = ""
    year_match = re.search(r'Year[:\s]+(\d{4})', html, re.IGNORECASE)
    if year_match:
        year = year_match.group(1)
    
    hours = ""
    hours_match = re.search(r'(?:Hours|Usage)[:\s]+(\d+)', html, re.IGNORECASE)
    if hours_match:
        hours = hours_match.group(1)
    
    return {'year': year, 'hours': hours}

# Load products
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# Build product info map
product_info = {}
for url in urls:
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    info = extract_product_info(url)
    product_info[clean_slug] = info

print(f"Loaded info for {len(product_info)} products\n")

# Fix index.html
print("Fixing index.html...")
with open('index.html', 'r') as f:
    content = f.read()

for slug, info in product_info.items():
    # Replace N/A values
    if info['year']:
        # Pattern: <span><strong>Year:</strong> N/A</span> within product card
        pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Year:</strong>\\s*)N/A(</span>)'
        content = re.sub(pattern, f'\\1{info["year"]}\\2', content, flags=re.DOTALL)
    
    if info['hours']:
        pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Hours:</strong>\\s*)N/A(</span>)'
        content = re.sub(pattern, f'\\1{info["hours"]}\\2', content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
print("✓ index.html fixed\n")

# Fix catalog.html
print("Fixing catalog.html...")
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, info in product_info.items():
    if info['year']:
        pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Year:</span>\\s*<span class="spec-value-compact">)N/A(</span>)'
        content = re.sub(pattern, f'\\1{info["year"]}\\2', content, flags=re.DOTALL)
    
    if info['hours']:
        pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Hours:</span>\\s*<span class="spec-value-compact">)N/A(</span>)'
        content = re.sub(pattern, f'\\1{info["hours"]}\\2', content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)
print("✓ catalog.html fixed\n")

print("✓ All N/A values replaced!")

