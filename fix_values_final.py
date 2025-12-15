#!/usr/bin/env python3
"""
Final fix - extract and apply correct Year and Hours for each product
"""

import re
import subprocess

# Product mapping with correct values
product_data = {}

with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print("Extracting correct values from source pages...\n")

for url in urls:
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    # Extract Year - try multiple patterns
    year = ""
    for pattern in [
        r'<li><span>Year:</span>\s*(\d{4})',
        r'Year[:\s]+(\d{4})',
        r'<strong>Year:</strong>\s*(\d{4})',
    ]:
        m = re.search(pattern, html, re.I)
        if m:
            year = m.group(1)
            break
    
    # Extract Hours - try multiple patterns  
    hours = ""
    for pattern in [
        r'<li><span>(?:Hours|Usage):</span>\s*(\d+)',
        r'(?:Hours|Usage)[:\s]+(\d+)',
        r'<strong>(?:Hours|Usage):</strong>\s*(\d+)',
    ]:
        m = re.search(pattern, html, re.I)
        if m:
            hours = m.group(1)
            break
    
    product_data[clean_slug] = {'year': year, 'hours': hours}
    print(f"  {clean_slug}: Year={year}, Hours={hours}")

print(f"\nProcessing {len(product_data)} products...\n")

# Fix index.html
print("Fixing index.html...")
with open('index.html', 'r') as f:
    content = f.read()

for slug, data in product_data.items():
    if not data['year'] or not data['hours']:
        continue
    
    # Replace in product card - match the exact structure
    old_pattern = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<div class="product-specs">.*?<span><strong>Year:</strong>\\s*)([^<]*?)(</span>.*?<span><strong>Hours:</strong>\\s*)([^<]*?)(</span>)'
    
    def replace_func(m):
        return m.group(1) + data['year'] + m.group(3) + data['hours'] + m.group(5)
    
    content = re.sub(old_pattern, replace_func, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
print("✓ index.html updated\n")

# Fix catalog.html
print("Fixing catalog.html...")
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, data in product_data.items():
    if data['year']:
        pattern = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Year:</span>\\s*<span class="spec-value-compact">)([^<]*?)(</span>)'
        content = re.sub(pattern, lambda m: m.group(1) + data['year'] + m.group(3), content, flags=re.DOTALL)
    
    if data['hours']:
        pattern = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Hours:</span>\\s*<span class="spec-value-compact">)([^<]*?)(</span>)'
        content = re.sub(pattern, lambda m: m.group(1) + data['hours'] + m.group(3), content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)
print("✓ catalog.html updated\n")

print("✓ All values corrected!")










