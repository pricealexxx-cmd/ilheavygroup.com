#!/usr/bin/env python3
"""
Fix missing Year and Hours in product pages by extracting from source
"""

import re
import subprocess
import os
import glob

def extract_product_info(url):
    """Extract Year and Hours from product page"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    # Try multiple patterns for Year
    year_patterns = [
        r'Year[:\s]+(\d{4})',
        r'<li><span>Year:</span>\s*(\d{4})',
        r'<strong>Year:</strong>\s*(\d{4})',
        r'Year[:\s]*</span>\s*(\d{4})',
    ]
    year = ""
    for pattern in year_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            year = match.group(1)
            break
    
    # Try multiple patterns for Hours
    hours_patterns = [
        r'(?:Hours|Usage)[:\s]+(\d+)',
        r'<li><span>(?:Hours|Usage):</span>\s*(\d+)',
        r'<strong>(?:Hours|Usage):</strong>\s*(\d+)',
        r'(?:Hours|Usage)[:\s]*</span>\s*(\d+)',
    ]
    hours = ""
    for pattern in hours_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            hours = match.group(1)
            break
    
    # Extract stock
    stock_patterns = [
        r'Stock[:\s]+(ZID-\d+)',
        r'<li><span>Stock[^<]*:</span>\s*(ZID-\d+)',
        r'<strong>Stock[^<]*:</strong>\s*(ZID-\d+)',
    ]
    stock = ""
    for pattern in stock_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            stock = match.group(1)
            break
    
    return {'year': year, 'hours': hours, 'stock': stock}

def update_product_page(filename, info):
    """Update product page with correct info"""
    with open(filename, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Update Year in info badges
    if info['year']:
        # Replace Year: with actual year
        content = re.sub(r'Year:\s*(\d{4}|)', f"Year: {info['year']}", content)
        content = re.sub(r'<span class="info-badge">Year:\s*</span>', f'<span class="info-badge">Year: {info["year"]}</span>', content)
        # Update in specs table
        content = re.sub(r'<td>Year</td>\s*<td></td>', f'<td>Year</td>\n                        <td>{info["year"]}</td>', content)
        content = re.sub(r'<td>Year</td>\s*<td>(\d{4})</td>', f'<td>Year</td>\n                        <td>{info["year"]}</td>', content)
    
    # Update Hours in info badges
    if info['hours']:
        # Replace Hours: with actual hours
        content = re.sub(r'Hours:\s*(\d+|)', f"Hours: {info['hours']}", content)
        content = re.sub(r'<span class="info-badge">Hours:\s*</span>', f'<span class="info-badge">Hours: {info["hours"]}</span>', content)
        # Update in specs table
        content = re.sub(r'<td>Usage Hours</td>\s*<td></td>', f'<td>Usage Hours</td>\n                        <td>{info["hours"]} Hours</td>', content)
        content = re.sub(r'<td>Usage Hours</td>\s*<td>(\d+ Hours)</td>', f'<td>Usage Hours</td>\n                        <td>{info["hours"]} Hours</td>', content)
        # Update in Quick Details
        content = re.sub(r'<li>✓ <strong>Hours:</strong> (\d+|)</li>', f'<li>✓ <strong>Hours:</strong> {info["hours"]}</li>', content)
    
    # Update Stock
    if info['stock']:
        content = re.sub(r'Stock:\s*(ZID-\d+|)', f"Stock: {info['stock']}", content)
        content = re.sub(r'<span class="info-badge">Stock:\s*</span>', f'<span class="info-badge">Stock: {info["stock"]}</span>', content)
        content = re.sub(r'<td>Stock Number</td>\s*<td></td>', f'<td>Stock Number</td>\n                        <td>{info["stock"]}</td>', content)
    
    if content != original_content:
        with open(filename, 'w') as f:
            f.write(content)
        return True
    return False

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Fixing product info for {len(urls)} products...\n")

updated_count = 0
for url in urls:
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    # Special case for first product
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    filename = f"product-{clean_slug}.html"
    
    if not os.path.exists(filename):
        continue
    
    try:
        info = extract_product_info(url)
        if update_product_page(filename, info):
            updated_count += 1
            print(f"  ✓ Updated: {clean_slug} (Year: {info['year']}, Hours: {info['hours']}, Stock: {info['stock']})")
    except Exception as e:
        print(f"  ✗ Error with {clean_slug}: {e}")

print(f"\n✓ Updated {updated_count} product pages")

