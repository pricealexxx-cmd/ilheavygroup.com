#!/usr/bin/env python3
"""
Final fix for contact.html - properly extract all products by category
"""

import re
from collections import defaultdict

# Read index.html
with open('index.html', 'r') as f:
    content = f.read()

products_by_category = defaultdict(list)

# Split by category sections more carefully
# Find each category section
category_sections = re.finditer(
    r'<!-- Category: ([^>]+) -->\s*<div[^>]*>\s*<h3 class="category-title">([^<]+)</h3>\s*<div class="products-grid"[^>]*>(.*?)</div>\s*</div>\s*</div>',
    content,
    re.DOTALL
)

for match in category_sections:
    category_comment = match.group(1).strip()
    category_title = match.group(2).strip()
    products_html = match.group(3)
    
    # Extract all product titles from this section
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

# Order categories
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

print("✓ Fixed contact.html")
for cat in category_order:
    if cat in products_by_category:
        print(f"  {cat}: {len(products_by_category[cat])} products")





