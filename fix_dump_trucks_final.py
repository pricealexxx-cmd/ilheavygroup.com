#!/usr/bin/env python3
"""
Final fix for Dump Trucks - replace all Hours with Miles
"""

import re
import os

# Dump Trucks with their mileages (formatted)
dump_trucks = {
    '2022-kenworth-t880-quad-axle-dump-truck': '85,000',
    '2020-peterbilt-389-tri-axle-dump-truck': '199,849',
    '2019-peterbilt-389-tri-axle-dump-truck': '168,751',
}

print("Fixing Dump Trucks pages...\n")

# Update product pages
for slug, miles in dump_trucks.items():
    filename = f"product-{slug}.html"
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Replace any remaining "hours" in descriptions
    content = re.sub(r'with only \d+ hours', f'with only {miles} miles', content)
    content = re.sub(r'only \d+ hours', f'only {miles} miles', content)
    
    # Ensure Miles is formatted correctly everywhere
    content = re.sub(r'Miles: (\d+)', f'Miles: {miles}', content)
    content = re.sub(r'<strong>Miles:</strong> (\d+)', f'<strong>Miles:</strong> {miles}', content)
    content = re.sub(r'(\d+) Miles</td>', f'{miles} Miles</td>', content)
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"✓ Fixed {filename}")

print("\nFixing index.html...\n")

# Update index.html
with open('index.html', 'r') as f:
    content = f.read()

for slug, miles in dump_trucks.items():
    # Simple replacement for product cards
    content = content.replace(f'<span><strong>Hours:</strong> 0</span>', f'<span><strong>Miles:</strong> {miles}</span>')
    # Also check for any other Hours values
    pattern = f'href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Hours:</strong>'
    if pattern in content:
        # Find the card and replace
        card_pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>)Hours(:</strong>\\s*)([^<]+)(</span>)'
        content = re.sub(card_pattern, f'\\1Miles\\2{miles}\\4', content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Fixed index.html")

print("\nFixing catalog.html...\n")

# Update catalog.html
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, miles in dump_trucks.items():
    # Simple replacement for product cards
    content = content.replace(f'<span><strong>Hours:</strong> 0</span>', f'<span><strong>Miles:</strong> {miles}</span>')
    # Also check for any other Hours values
    card_pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>)Hours(:</strong>\\s*)([^<]+)(</span>)'
    content = re.sub(card_pattern, f'\\1Miles\\2{miles}\\4', content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)

print("✓ Fixed catalog.html")

print("\n✓ All Dump Trucks fixed!")





