#!/usr/bin/env python3
"""
Fix Year and Hours in product cards on index.html and catalog.html
"""

import re
import subprocess
import json
import os

def extract_product_info(url):
    """Extract Year and Hours from product page"""
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

# Load categorized products
with open('products_categorized.txt', 'r') as f:
    products_by_category = json.load(f)

# Get all products with their info
all_products = {}
for category, products in products_by_category.items():
    for product in products:
        slug = product['slug']
        url = product['url']
        info = extract_product_info(url)
        all_products[slug] = {
            'year': info['year'],
            'hours': info['hours'],
            'title': product['title']
        }

print(f"Extracted info for {len(all_products)} products\n")

# Update index.html
print("Updating index.html...")
with open('index.html', 'r') as f:
    content = f.read()

for slug, info in all_products.items():
    # Update Year in product specs - find the product card section
    if info['year']:
        # Pattern for index.html product cards
        pattern1 = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Year:</strong>\\s*)([^<]*?)(</span>)'
        def replace_year1(m):
            return m.group(1) + info['year'] + m.group(3)
        content = re.sub(pattern1, replace_year1, content, flags=re.DOTALL)
        
        # Pattern for N/A values
        pattern2 = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Year:</strong>\\s*)(N/A|)(</span>)'
        def replace_year2(m):
            return m.group(1) + info['year'] + m.group(3)
        content = re.sub(pattern2, replace_year2, content, flags=re.DOTALL)
    
    # Update Hours in product specs
    if info['hours']:
        pattern1 = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Hours:</strong>\\s*)([^<]*?)(</span>)'
        def replace_hours1(m):
            return m.group(1) + info['hours'] + m.group(3)
        content = re.sub(pattern1, replace_hours1, content, flags=re.DOTALL)
        
        pattern2 = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Hours:</strong>\\s*)(N/A|)(</span>)'
        def replace_hours2(m):
            return m.group(1) + info['hours'] + m.group(3)
        content = re.sub(pattern2, replace_hours2, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
print("✓ index.html updated\n")

# Update catalog.html
print("Updating catalog.html...")
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, info in all_products.items():
    # Update in compact cards
    if info['year']:
        pattern1 = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Year:</span>\\s*<span class="spec-value-compact">)([^<]*?)(</span>)'
        def replace_year1(m):
            return m.group(1) + info['year'] + m.group(3)
        content = re.sub(pattern1, replace_year1, content, flags=re.DOTALL)
        
        pattern2 = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Year:</span>\\s*<span class="spec-value-compact">)(N/A|)(</span>)'
        def replace_year2(m):
            return m.group(1) + info['year'] + m.group(3)
        content = re.sub(pattern2, replace_year2, content, flags=re.DOTALL)
    
    if info['hours']:
        pattern1 = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Hours:</span>\\s*<span class="spec-value-compact">)([^<]*?)(</span>)'
        def replace_hours1(m):
            return m.group(1) + info['hours'] + m.group(3)
        content = re.sub(pattern1, replace_hours1, content, flags=re.DOTALL)
        
        pattern2 = f'(<a href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span class="spec-label-compact">Hours:</span>\\s*<span class="spec-value-compact">)(N/A|)(</span>)'
        def replace_hours2(m):
            return m.group(1) + info['hours'] + m.group(3)
        content = re.sub(pattern2, replace_hours2, content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)
print("✓ catalog.html updated\n")

print("✓ All cards updated!")

