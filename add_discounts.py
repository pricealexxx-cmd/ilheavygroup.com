#!/usr/bin/env python3
"""
Add discounts (15-20%) to all products added today
Update cards and product pages with old price (strikethrough) and new price
"""

import re
import subprocess
import os
import random

def extract_price(price_str):
    """Extract numeric price from string"""
    # Remove $ and commas
    price_clean = price_str.replace('$', '').replace(',', '').strip()
    # Extract first number
    match = re.search(r'(\d+)', price_clean)
    if match:
        return int(match.group(1))
    return None

def format_price(price):
    """Format price with $ and commas"""
    return f"${price:,}"

def calculate_discount_price(original_price, discount_percent):
    """Calculate price after discount"""
    return int(original_price * (1 - discount_percent / 100))

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print("Processing discounts for products...\n")

product_discounts = {}

for url in urls:
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    if not os.path.exists(f"images/{clean_slug}"):
        continue
    
    # Get product info
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    # Extract price
    price_match = re.search(r'\$([0-9,]+)', html)
    if price_match:
        original_price_str = price_match.group(0)
        original_price = extract_price(original_price_str)
        
        if original_price:
            # Random discount between 15-20%
            discount = random.uniform(15, 20)
            new_price = calculate_discount_price(original_price, discount)
            
            product_discounts[clean_slug] = {
                'original': original_price_str,
                'original_num': original_price,
                'new_num': new_price,
                'new': format_price(new_price),
                'discount': round(discount, 1)
            }
            
            print(f"  {clean_slug}: {original_price_str} -> {format_price(new_price)} ({discount:.1f}% off)")

print(f"\n✓ Processed {len(product_discounts)} products\n")

# Update index.html
print("Updating index.html...")
with open('index.html', 'r') as f:
    content = f.read()

for slug, prices in product_discounts.items():
    # Find product card and update price
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<p style="color: var\\(--primary-color\\); font-weight: 600; font-size: 1\\.1rem; margin: 0\\.5rem 0;">)([^<]+)(</p>)'
    
    def replacer(m):
        old_price_html = f'<span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{prices["original"]}</span><span style="color: #dc2626; font-weight: 700;">{prices["new"]}</span>'
        return m.group(1) + old_price_html + m.group(3)
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Updated index.html\n")

# Update catalog.html
print("Updating catalog.html...")
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, prices in product_discounts.items():
    # Find product card and update price
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)([^<]+)(</p>)'
    
    def replacer(m):
        old_price_html = f'<span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{prices["original"]}</span><span style="color: #dc2626; font-weight: 700;">{prices["new"]}</span>'
        return m.group(1) + old_price_html + m.group(3)
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)

print("✓ Updated catalog.html\n")

# Update product pages
print("Updating product pages...")
for slug, prices in product_discounts.items():
    filename = f"product-{slug}.html"
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Update price in product page
    # Find price in h1 area or price section
    price_patterns = [
        (r'(\$[0-9,]+)\s*USD', f'<span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{prices["original"]} USD</span><span style="color: #dc2626; font-weight: 700; font-size: 1.2em;">{prices["new"]} USD</span>'),
        (r'<p[^>]*style="[^"]*color[^"]*var\\(--primary-color\\)[^"]*"[^>]*>(\$[0-9,]+)</p>', f'<p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;"><span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{prices["original"]}</span><span style="color: #dc2626; font-weight: 700;">{prices["new"]}</span></p>'),
    ]
    
    for pattern, replacement in price_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            break
    
    # Also add discount badge if not exists
    if 'discount-badge' not in content.lower():
        # Add discount info near price
        discount_badge = f'<div style="background: #dc2626; color: white; padding: 0.5rem 1rem; border-radius: 5px; display: inline-block; margin-left: 1rem; font-weight: 600;">Save {prices["discount"]}%</div>'
        # Try to add after price
        content = re.sub(
            r'(<p[^>]*style="[^"]*color[^"]*var\\(--primary-color\\)[^"]*"[^>]*>.*?</p>)',
            r'\1' + discount_badge,
            content,
            count=1
        )
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"  ✓ Updated {filename}")

print(f"\n✓ All {len(product_discounts)} product pages updated!")
print("\n✓ Discounts applied successfully!")

