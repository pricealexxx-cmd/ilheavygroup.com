#!/usr/bin/env python3
"""
Final fix: Remove discounts from Bobcat, add to all others with discount percentage
"""

import re
import os

# Original prices
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

# Discount prices (from previous run)
discount_prices = {
    'caterpillar-299d3-2022': {'new': '$42,585', 'discount': 15.3},
    '2018-caterpillar-320gc': {'new': '$61,391', 'discount': 17.8},
    '2018-caterpillar-420f2-backhoe': {'new': '$40,889', 'discount': 18.2},
    '2023-john-deere-770gp-motor-grader': {'new': '$161,989', 'discount': 17.8},
    '2015-caterpillar-backhoe-loader-420f2-it': {'new': '$38,116', 'discount': 15.7},
    '2019-caterpillar-313flgc': {'new': '$51,523', 'discount': 18.3},
    '2018-caterpillar-320': {'new': '$66,655', 'discount': 17.0},
    '2019-caterpillar-312f': {'new': '$42,177', 'discount': 17.3},
    '2017-caterpillar-excavator-316fl': {'new': '$45,978', 'discount': 17.0},
    '2021-kubota-u55-5-mini-excavator': {'new': '$33,704', 'discount': 16.8},
    '2022-kubota-u50-5-mini-excavator': {'new': '$29,398', 'discount': 18.1},
    '2021-kubota-u48-5-mini-excavator': {'new': '$36,944', 'discount': 15.3},
    '2022-kubota-kx-040-4-mini-excavator': {'new': '$32,730', 'discount': 18.8},
    '2024-kubota-svl97-2hfc-compact-track-loader': {'new': '$37,004', 'discount': 17.6},
    '2024-kubota-svl97-2-compact-track-loader': {'new': '$34,861', 'discount': 16.6},
    '2020-kubota-svl95-2shfc-compact-track-loader': {'new': '$28,662', 'discount': 18.3},
    '2022-caterpillar-259d3-skid-steer-loader': {'new': '$37,747', 'discount': 18.8},
    'deere-331g-skid-steer-track': {'new': '$37,396', 'discount': 16.7},
    '2022-caterpillar-skid-steer-259d3': {'new': '$39,774', 'discount': 18.0},
    '2019-kubota-svl75-2-skid-steer': {'new': '$31,080', 'discount': 19.3},
    '2019-john-deere-8245r-tractor': {'new': '$76,349', 'discount': 16.8},
    '2019-caterpillar-tl1255d-telehandler': {'new': '$41,028', 'discount': 17.9},
    '2022-jlg-925-telehandler': {'new': '$41,247', 'discount': 19.8},
    '2023-jcb-510-56-telehandler-2': {'new': '$41,579', 'discount': 16.0},
    '2023-caterpillar-tl1055-telehandler': {'new': '$59,547', 'discount': 15.5},
    '2022-kenworth-t880-quad-axle-dump-truck': {'new': '$85,558', 'discount': 15.4},
    '2020-peterbilt-389-tri-axle-dump-truck': {'new': '$51,443', 'discount': 17.8},
    '2019-peterbilt-389-tri-axle-dump-truck': {'new': '$62,623', 'discount': 15.6},
}

# Bobcat products - NO discounts
bobcat_products = ['2021-bobcat-t870-skid-steer-track', '2024-bobcat-t86-compact-track-loader', '2023-bobcat-t770-track-skid-steer']

print("Fixing discounts...\n")

# Update index.html
with open('index.html', 'r') as f:
    content = f.read()

# Remove discounts from Bobcat products
for slug in bobcat_products:
    original = original_prices.get(slug, '')
    if original:
        # Remove any discount display
        pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<p style="color: var\\(--primary-color\\); font-weight: 600; font-size: 1\\.1rem; margin: 0\\.5rem 0;">)(<span[^>]*>.*?</span><span[^>]*>.*?</span>.*?</p>)'
        def replacer(m):
            return m.group(1) + original + '</p>'
        content = re.sub(pattern, replacer, content, flags=re.DOTALL)

# Add/update discounts for non-Bobcat products
for slug, discount_info in discount_prices.items():
    original = original_prices.get(slug, '')
    if not original or '$' not in original:
        continue
    
    old_price_html = f'<span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{original}</span><span style="color: #dc2626; font-weight: 700;">{discount_info["new"]}</span> <span style="background: #dc2626; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.85em; font-weight: 600; margin-left: 0.5rem;">-{discount_info["discount"]}%</span>'
    
    # Replace simple price or existing discount
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<p style="color: var\\(--primary-color\\); font-weight: 600; font-size: 1\\.1rem; margin: 0\\.5rem 0;">)([^<]+)(</p>)'
    def replacer(m):
        return m.group(1) + old_price_html + m.group(3)
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Updated index.html\n")

# Update catalog.html
with open('catalog.html', 'r') as f:
    content = f.read()

# Remove discounts from Bobcat
for slug in bobcat_products:
    original = original_prices.get(slug, '')
    if original:
        pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)(<span[^>]*>.*?</span><span[^>]*>.*?</span>.*?</p>)'
        def replacer(m):
            return m.group(1) + original + '</p>'
        content = re.sub(pattern, replacer, content, flags=re.DOTALL)

# Add discounts for non-Bobcat
for slug, discount_info in discount_prices.items():
    original = original_prices.get(slug, '')
    if not original or '$' not in original:
        continue
    
    old_price_html = f'<span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{original}</span><span style="color: #dc2626; font-weight: 700;">{discount_info["new"]}</span> <span style="background: #dc2626; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.85em; font-weight: 600; margin-left: 0.5rem;">-{discount_info["discount"]}%</span>'
    
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<p[^>]*style="[^"]*color[^"]*"[^>]*>)([^<]+)(</p>)'
    def replacer(m):
        return m.group(1) + old_price_html + m.group(3)
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)

print("✓ Updated catalog.html\n")

# Update product pages
print("Updating product pages...")
for slug, discount_info in discount_prices.items():
    filename = f"product-{slug}.html"
    if not os.path.exists(filename):
        continue
    
    original = original_prices.get(slug, '')
    if not original or '$' not in original:
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    old_price_html = f'<span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{original} USD</span><span style="color: #dc2626; font-weight: 700; font-size: 1.2em;">{discount_info["new"]} USD</span><div style="background: #dc2626; color: white; padding: 0.5rem 1rem; border-radius: 5px; display: inline-block; margin-left: 1rem; font-weight: 600; font-size: 0.9em;">Save {discount_info["discount"]}%</div>'
    
    content = re.sub(
        r'<div class="price-badge">.*?</div>',
        f'<div class="price-badge">{old_price_html}</div>',
        content,
        flags=re.DOTALL
    )
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"  ✓ Updated {filename}")

# Remove discounts from Bobcat product pages
for slug in bobcat_products:
    filename = f"product-{slug}.html"
    if not os.path.exists(filename):
        continue
    
    original = original_prices.get(slug, '')
    if not original:
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Remove discount, restore simple price
    simple_price = f'{original} USD' if '$' in original else original
    content = re.sub(
        r'<div class="price-badge">.*?</div>',
        f'<div class="price-badge">{simple_price}</div>',
        content,
        flags=re.DOTALL
    )
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"  ✓ Removed discount from {filename}")

print(f"\n✓ All products updated!")
print(f"  - {len(discount_prices)} products WITH discounts (15-20%)")
print(f"  - {len(bobcat_products)} Bobcat products WITHOUT discounts")

