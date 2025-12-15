#!/usr/bin/env python3
"""
Remove all discounts from Bobcat products
"""

import re
import os

# Original prices for Bobcat products
bobcat_products = {
    '2021-bobcat-t870-skid-steer-track': '$48,500',
    '2024-bobcat-t86-compact-track-loader': '$47,100',
    '2023-bobcat-t770-track-skid-steer': '$41,000',
    't450': '$57,000 - $70,000',  # Old products
    't590': '$72,000 - $85,000',
    't770': 'Price varies',
    't870': 'Price varies',
}

print("Removing discounts from all Bobcat products...\n")

# Update index.html
with open('index.html', 'r') as f:
    content = f.read()

# Find all Bobcat product cards and remove discounts
# Pattern: any product card with "bobcat" in href or title
bobcat_pattern = r'(href="product-[^"]*bobcat[^"]*\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)(<span[^>]*text-decoration: line-through[^>]*>.*?</span><span[^>]*>.*?</span>.*?</p>)'

def remove_discount(match):
    # Extract the original price from the strikethrough span
    full_match = match.group(0)
    # Try to find original price in strikethrough
    price_match = re.search(r'<span[^>]*text-decoration: line-through[^>]*>(\$[0-9,]+)', full_match)
    if price_match:
        original_price = price_match.group(1)
        # Replace the whole price section with just original price
        return match.group(1) + original_price + '</p>'
    return match.group(1) + match.group(2)

content = re.sub(bobcat_pattern, remove_discount, content, flags=re.DOTALL | re.IGNORECASE)

# Also handle old Bobcat products (t450, t590, etc.)
old_bobcat_patterns = [
    (r'(href="product-t450\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)(<span[^>]*>.*?</span><span[^>]*>.*?</span>.*?</p>)', '$57,000 - $70,000'),
    (r'(href="product-t590\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)(<span[^>]*>.*?</span><span[^>]*>.*?</span>.*?</p>)', '$72,000 - $85,000'),
    (r'(href="product-t770\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)(<span[^>]*>.*?</span><span[^>]*>.*?</span>.*?</p>)', 'Contact for Price'),
    (r'(href="product-t870\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)(<span[^>]*>.*?</span><span[^>]*>.*?</span>.*?</p>)', 'Contact for Price'),
]

for pattern, price in old_bobcat_patterns:
    def replacer(m):
        return m.group(1) + price + '</p>'
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Updated index.html\n")

# Update catalog.html
with open('catalog.html', 'r') as f:
    content = f.read()

bobcat_pattern = r'(href="product-[^"]*bobcat[^"]*\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)(<span[^>]*text-decoration: line-through[^>]*>.*?</span><span[^>]*>.*?</span>.*?</p>)'
content = re.sub(bobcat_pattern, remove_discount, content, flags=re.DOTALL | re.IGNORECASE)

for pattern, price in old_bobcat_patterns:
    def replacer(m):
        return m.group(1) + price + '</p>'
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)

print("✓ Updated catalog.html\n")

# Update product pages
print("Updating product pages...")
for filename in os.listdir('.'):
    if filename.startswith('product-') and filename.endswith('.html'):
        if 'bobcat' not in filename.lower():
            continue
        
        with open(filename, 'r') as f:
            content = f.read()
        
        # Remove discount from price badge
        # Find original price in strikethrough
        price_match = re.search(r'<span[^>]*text-decoration: line-through[^>]*>(\$[0-9,]+) USD</span>', content)
        if price_match:
            original_price = price_match.group(1)
            # Replace price badge with simple price
            content = re.sub(
                r'<div class="price-badge">.*?</div>',
                f'<div class="price-badge">{original_price} USD</div>',
                content,
                flags=re.DOTALL
            )
        
        # Also remove from paragraphs
        content = re.sub(
            r'<p[^>]*style="[^"]*color[^"]*var\\(--primary-color\\)[^"]*"[^>]*><span[^>]*text-decoration: line-through[^>]*>.*?</span><span[^>]*>.*?</span>.*?</p>',
            lambda m: re.sub(r'<span[^>]*text-decoration: line-through[^>]*>(\$[0-9,]+)</span>', r'\1', m.group(0)),
            content,
            flags=re.DOTALL
        )
        
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"  ✓ Updated {filename}")

print(f"\n✓ All Bobcat products updated - discounts removed!")










