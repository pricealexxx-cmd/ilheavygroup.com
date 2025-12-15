#!/usr/bin/env python3
"""
Replace Hours with Miles for all Dump Trucks
"""

import re
import subprocess
import os

def extract_mileage(url):
    """Extract mileage from source page"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    # Try to find mileage
    mileage = ""
    for pattern in [
        r'<li><span>Mileage:</span>\s*([0-9,]+)',
        r'<strong[^>]*>Miles:</strong>\s*([0-9,]+)',
        r'Mileage[:\s]+([0-9,]+)',
        r'<strong[^>]*>([0-9,]+)\s*miles</strong>',
    ]:
        match = re.search(pattern, html, re.I)
        if match:
            mileage = match.group(1).replace(',', '')
            break
    
    return mileage

# Dump Trucks URLs
dump_trucks = {
    '2022-kenworth-t880-quad-axle-dump-truck': 'https://johnstractorhouse.com/equipment/2022-kenworth-t880-quad-axle-dump-truck/',
    '2020-peterbilt-389-tri-axle-dump-truck': 'https://johnstractorhouse.com/equipment/2020-peterbilt-389-tri-axle-dump-truck/',
    '2019-peterbilt-389-tri-axle-dump-truck': 'https://johnstractorhouse.com/equipment/2019-peterbilt-389-tri-axle-dump-truck/',
}

print("Extracting mileage for Dump Trucks...\n")

mileage_data = {}
for slug, url in dump_trucks.items():
    mileage = extract_mileage(url)
    mileage_data[slug] = mileage
    print(f"{slug}: {mileage} miles")

print("\nUpdating product pages...\n")

# Update product pages
for slug, mileage in mileage_data.items():
    if not mileage:
        print(f"⚠ No mileage found for {slug}, skipping")
        continue
    
    filename = f"product-{slug}.html"
    if not os.path.exists(filename):
        print(f"⚠ File not found: {filename}")
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Replace Hours with Miles in info badges
    content = re.sub(r'<span class="info-badge">Hours: \d+</span>', 
                    f'<span class="info-badge">Miles: {mileage}</span>', content)
    
    # Replace in Quick Details
    content = re.sub(r'<li>✓ <strong>Hours:</strong> \d+</li>', 
                    f'<li>✓ <strong>Miles:</strong> {mileage}</li>', content)
    
    # Replace in specs table
    content = re.sub(r'<td>Usage Hours</td>\s*<td>\d+ Hours</td>', 
                    f'<td>Mileage</td>\n                        <td>{mileage} Miles</td>', content)
    
    # Replace in description
    content = re.sub(r'With only <strong>\d+ hours</strong>', 
                    f'With only <strong>{mileage} miles</strong>', content)
    
    # Replace in product-specs divs
    content = re.sub(r'<span><strong>Hours:</strong> \d+</span>', 
                    f'<span><strong>Miles:</strong> {mileage}</span>', content)
    
    # Update h1 and title if needed
    content = re.sub(r'<h1>[^<]+</h1>', 
                    lambda m: m.group(0) if 'Dump Truck' not in m.group(0) else m.group(0), content)
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated {filename}")

print("\nUpdating index.html...\n")

# Update index.html
with open('index.html', 'r') as f:
    content = f.read()

for slug, mileage in mileage_data.items():
    if not mileage:
        continue
    
    # Replace in product cards
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Hours:</strong>\\s*)([^<]+)(</span>)'
    
    def replacer(m):
        return m.group(1) + mileage + m.group(3)
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    # Also replace the label
    content = re.sub(f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>)Hours(:</strong>\\s*{mileage}</span>)', 
                    r'\1Miles\2', content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Updated index.html")

print("\nUpdating catalog.html...\n")

# Update catalog.html
with open('catalog.html', 'r') as f:
    content = f.read()

for slug, mileage in mileage_data.items():
    if not mileage:
        continue
    
    # Replace in product cards
    pattern = f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>Hours:</strong>\\s*)([^<]+)(</span>)'
    
    def replacer(m):
        return m.group(1) + mileage + m.group(3)
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    # Also replace the label
    content = re.sub(f'(href="product-{re.escape(slug)}\\.html"[^>]*>.*?<span><strong>)Hours(:</strong>\\s*{mileage}</span>)', 
                    r'\1Miles\2', content, flags=re.DOTALL)

with open('catalog.html', 'w') as f:
    f.write(content)

print("✓ Updated catalog.html")

print("\n✓ All Dump Trucks updated with Miles instead of Hours!")










