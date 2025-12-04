#!/usr/bin/env python3
"""
Add all products to catalog and index pages
"""

import re
import subprocess
import os

def get_product_info(url):
    """Get basic product info"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    price = re.search(r'\$([0-9,]+)', html)
    price = price.group(0) if price else "Contact for Price"
    
    year = re.search(r'Year[:\s]+(\d{4})', html, re.I)
    year = year.group(1) if year else ""
    
    hours = re.search(r'(?:Hours|Usage)[:\s]+(\d+)', html, re.I)
    hours = hours.group(1) if hours else ""
    
    title = re.search(r'<title>([^<]+)', html)
    title = title.group(1).split('|')[0].strip() if title else ""
    title = title.replace('&#8212;', '-').replace('&amp;', '&')
    
    stock = re.search(r'Stock[:\s]+(ZID-\d+)', html, re.I)
    stock = stock.group(1) if stock else ""
    
    return {'title': title, 'price': price, 'year': year, 'hours': hours, 'stock': stock}

def categorize_product(title, url):
    """Determine product category"""
    title_lower = title.lower()
    url_lower = url.lower()
    combined = title_lower + ' ' + url_lower
    
    # Check in order of specificity
    if 'backhoe' in combined:
        return 'Backhoes'
    elif 'telehandler' in combined or 'tl1255' in combined or 'tl1055' in combined or 'jlg' in combined or 'jcb-510' in combined:
        return 'Telehandlers'
    elif 'dump truck' in combined or 'kenworth' in combined or 'peterbilt' in combined:
        return 'Dump Trucks'
    elif 'motor grader' in combined or '770gp' in combined:
        return 'Motor Graders'
    elif 'tractor' in combined:
        if '8245' in combined or '6175' in combined or 'row crop' in combined:
            return 'Row Crop Tractors'
        return 'Sub-Compact Tractors'
    elif 'excavator' in combined or 'u55' in combined or 'u50' in combined or 'u48' in combined or 'kx-040' in combined or '316fl' in combined or '312f' in combined or '313flgc' in combined or '320' in combined or '320gc' in combined:
        return 'Compact (Mini) Excavators'
    elif 'skid steer' in combined or 'track loader' in combined or 't870' in combined or 't86' in combined or 't770' in combined or 'svl' in combined or '259d' in combined or '299d' in combined or '331g' in combined:
        return 'Compact Track Loaders'
    elif 'compressor' in combined:
        return 'Portable Air Compressors'
    elif 'mower' in combined:
        return 'Zero-Turn Mowers'
    
    return 'Compact Track Loaders'  # Default

# Read products
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Adding {len(urls)} products to catalog...\n")

products_by_category = {}

for url in urls:
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    # Special case for first product
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    if not os.path.exists(f"images/{clean_slug}"):
        continue
    
    try:
        info = get_product_info(url)
        category = categorize_product(info['title'], url)
        
        if category not in products_by_category:
            products_by_category[category] = []
        
        products_by_category[category].append({
            'slug': clean_slug,
            'url': url,
            **info
        })
        print(f"  ✓ {info['title'][:50]} -> {category}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print(f"\n✓ Categorized {sum(len(v) for v in products_by_category.values())} products")
print(f"Categories: {', '.join(products_by_category.keys())}")

# Save to file for next step
with open('products_categorized.txt', 'w') as f:
    import json
    json.dump(products_by_category, f, indent=2)

print("\n✓ Products categorized and saved!")

