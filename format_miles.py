#!/usr/bin/env python3
"""
Format miles with commas for better readability
"""

import re
import os

# Dump Trucks with their mileages
dump_trucks = {
    '2022-kenworth-t880-quad-axle-dump-truck': '85,000',
    '2020-peterbilt-389-tri-axle-dump-truck': '199,849',
    '2019-peterbilt-389-tri-axle-dump-truck': '168,751',
}

print("Formatting miles with commas...\n")

# Update product pages
for slug, formatted_miles in dump_trucks.items():
    filename = f"product-{slug}.html"
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Replace unformatted miles with formatted
    content = re.sub(r'Miles: (\d+)', f'Miles: {formatted_miles}', content)
    content = re.sub(r'<strong>Miles:</strong> (\d+)', f'<strong>Miles:</strong> {formatted_miles}', content)
    content = re.sub(r'(\d+) Miles</td>', f'{formatted_miles} Miles</td>', content)
    content = re.sub(r'<strong>(\d+) miles</strong>', f'<strong>{formatted_miles} miles</strong>', content)
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"✓ Formatted {filename}")

# Update index.html
with open('index.html', 'r') as f:
    content = f.read()

for slug, formatted_miles in dump_trucks.items():
    # Replace in product cards
    content = re.sub(f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Miles:</strong>\\s*)(\\d+)(</span>)', 
                    f'\\1{formatted_miles}\\3', content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Formatted index.html")

# Update catalog.html
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, formatted_miles in dump_trucks.items():
    # Replace in product cards
    content = re.sub(f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Miles:</strong>\\s*)(\\d+)(</span>)', 
                    f'\\1{formatted_miles}\\3', content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)

print("✓ Formatted catalog.html")

print("\n✓ All miles formatted with commas!")










