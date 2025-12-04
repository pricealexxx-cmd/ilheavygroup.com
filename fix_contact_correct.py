#!/usr/bin/env python3
"""
Correctly extract products by matching category sections properly
"""

import re
from collections import defaultdict

# Read index.html
with open('index.html', 'r') as f:
    content = f.read()

products_by_category = defaultdict(list)

# Find category sections more precisely
# Pattern: <!-- Category: NAME --> ... <h3 class="category-title">TITLE</h3> ... products ...
sections = content.split('<!-- Category:')

for i, section in enumerate(sections[1:], 1):  # Skip first empty split
    # Extract category name from comment
    category_match = re.search(r'^([^>]+) -->', section)
    if not category_match:
        continue
    
    # Extract category title
    title_match = re.search(r'<h3 class="category-title">([^<]+)</h3>', section)
    if not title_match:
        continue
    
    category_title = title_match.group(1).strip()
    
    # Extract products from this section (until next category or end)
    # Find products-grid div
    grid_match = re.search(r'<div class="products-grid"[^>]*>(.*?)(?=<!-- Category:|</div>\s*</div>\s*</div>\s*<!-- Category:|$)', section, re.DOTALL)
    if grid_match:
        products_html = grid_match.group(1)
        # Extract all h3 tags (product titles)
        product_titles = re.findall(r'<h3>([^<]+)</h3>', products_html)
        for title in product_titles:
            title = title.strip()
            if title:
                products_by_category[category_title].append(title)

# Remove duplicates and sort
for cat in products_by_category:
    products_by_category[cat] = sorted(list(set(products_by_category[cat])))

# Read contact.html
with open('contact.html', 'r') as f:
    contact_content = f.read()

# Generate options
product_options = ['                                <option value="">-- Select Product --</option>\n']

category_order = [
    'Backhoes',
    'Motor Graders',
    'Telehandlers',
    'Dump Trucks',
    'Compact Track Loaders',
    'Portable Air Compressors',
    'Sub-Compact Tractors',
    'Row Crop Tractors',
    'Compact (Mini) Excavators',
    'Zero-Turn Mowers',
]

for category in category_order:
    if category in products_by_category and products_by_category[category]:
        product_options.append(f'                                <optgroup label="{category}">\n')
        for product in products_by_category[category]:
            product_options.append(f'                                    <option value="{product}">{product}</option>\n')
        product_options.append('                                </optgroup>\n')

product_options.append('                                <option value="Other">Other Equipment</option>\n')
product_options.append('                                <option value="General">General Inquiry</option>\n')

new_select_content = ''.join(product_options)

# Replace
select_pattern = r'(<select id="product" name="product">)(.*?)(</select>)'
contact_content = re.sub(select_pattern, r'\1\n' + new_select_content + '                            \3', contact_content, flags=re.DOTALL)

# Write
with open('contact.html', 'w') as f:
    f.write(contact_content)

print("✓ Fixed contact.html with correct categories")
for cat in category_order:
    if cat in products_by_category:
        print(f"  {cat}: {len(products_by_category[cat])} products")
        # Show first product as example
        if products_by_category[cat]:
            print(f"    Example: {products_by_category[cat][0]}")

