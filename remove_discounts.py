#!/usr/bin/env python3
"""
Remove discounts from all new products - restore original prices
"""

import re
import os

# Original prices for all products
original_prices = {
    'caterpillar-299d3-2022': '$50,300',
    '2021-bobcat-t870-skid-steer-track': '$48,500',
    '2018-caterpillar-320gc': '$74,700',
    '2018-caterpillar-420f2-backhoe': '$50,000',
    '2023-john-deere-770gp-motor-grader': '$197,000',
    '2015-caterpillar-backhoe-loader-420f2-it': '$45,200',
    '2016-caterpillar-backhoe-loader-420f2-it': 'Contact for Price',
    '2024-john-deere-310-p-tier-4x4-backhoe-loader': 'Contact for Price',
    '2019-caterpillar-313flgc': '$63,100',
    '2018-caterpillar-320': '$80,300',
    '2019-caterpillar-312f': '$51,000',
    '2017-caterpillar-excavator-316fl': '$55,400',
    '2021-kubota-u55-5-mini-excavator': '$40,500',
    '2022-kubota-u50-5-mini-excavator': '$35,900',
    '2021-kubota-u48-5-mini-excavator': '$43,600',
    '2022-kubota-kx-040-4-mini-excavator': '$40,300',
    '2024-bobcat-t86-compact-track-loader': '$47,100',
    '2024-kubota-svl97-2hfc-compact-track-loader': '$44,900',
    '2024-kubota-svl97-2-compact-track-loader': '$41,800',
    '2020-kubota-svl95-2shfc-compact-track-loader': '$35,100',
    '2022-caterpillar-259d3-skid-steer-loader': '$46,500',
    'deere-331g-skid-steer-track': '$44,900',
    '2022-caterpillar-skid-steer-259d3': '$48,500',
    '2019-kubota-svl75-2-skid-steer': '$38,500',
    '2023-bobcat-t770-track-skid-steer': '$41,000',
    '2019-john-deere-8245r-tractor': '$91,800',
    '2019-caterpillar-tl1255d-telehandler': '$50,000',
    '2022-jlg-925-telehandler': '$51,400',
    '2023-jcb-510-56-telehandler-2': '$49,500',
    '2023-caterpillar-tl1055-telehandler': '$70,500',
    '2022-kenworth-t880-quad-axle-dump-truck': '$101,100',
    '2020-peterbilt-389-tri-axle-dump-truck': '$62,600',
    '2019-peterbilt-389-tri-axle-dump-truck': '$74,200',
}

print("Removing discounts from all products...\n")

# Update index.html
print("Updating index.html...")
with open('index.html', 'r') as f:
    content = f.read()

for slug, original_price in original_prices.items():
    # Remove discount price display - restore to simple price
    # Pattern: <span style="text-decoration: line-through...">old</span><span style="color: #dc2626...">new</span>
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<p style="color: var\\(--primary-color\\); font-weight: 600; font-size: 1\\.1rem; margin: 0\\.5rem 0;">)(<span[^>]*>.*?</span><span[^>]*>.*?</span>)(</p>)'
    
    def replacer(m):
        return m.group(1) + original_price + m.group(3)
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Updated index.html\n")

# Update catalog.html
print("Updating catalog.html...")
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, original_price in original_prices.items():
    # Remove discount price display
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)(<span[^>]*>.*?</span><span[^>]*>.*?</span>)(</p>)'
    
    def replacer(m):
        return m.group(1) + original_price + m.group(3)
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)

print("✓ Updated catalog.html\n")

# Update product pages
print("Updating product pages...")
for slug, original_price in original_prices.items():
    filename = f"product-{slug}.html"
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Remove discount from price badge
    # Replace complex price badge with simple price
    simple_price = f'{original_price} USD' if '$' in original_price else original_price
    content = re.sub(
        r'<div class="price-badge">.*?</div>',
        f'<div class="price-badge">{simple_price}</div>',
        content,
        flags=re.DOTALL
    )
    
    # Also fix any price in paragraphs
    content = re.sub(
        r'<p[^>]*style="[^"]*color[^"]*var\\(--primary-color\\)[^"]*"[^>]*><span[^>]*>.*?</span><span[^>]*>.*?</span></p>',
        f'<p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;">{original_price}</p>',
        content,
        flags=re.DOTALL
    )
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"  ✓ Updated {filename}")

print(f"\n✓ All {len(original_prices)} products updated - discounts removed!")





