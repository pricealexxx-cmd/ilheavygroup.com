#!/usr/bin/env python3
"""
Fix contact.html product list - extract all products correctly from index.html
"""

import re
from collections import defaultdict

# Read index.html
with open('index.html', 'r') as f:
    content = f.read()

# Extract products by category more carefully
products_by_category = defaultdict(list)

# Find all category sections
sections = re.finditer(
    r'<!-- Category: ([^>]+) -->.*?<h3 class="category-title">([^<]+)</h3>.*?<div class="products-grid"[^>]*>(.*?)</div>\s*</div>\s*</div>',
    content,
    re.DOTALL
)

for match in sections:
    category_comment = match.group(1).strip()
    category_title = match.group(2).strip()
    products_html = match.group(3)
    
    # Extract product titles
    product_titles = re.findall(r'<h3>([^<]+)</h3>', products_html)
    
    for title in product_titles:
        title = title.strip()
        if title and title not in products_by_category[category_title]:
            products_by_category[category_title].append(title)

# Category mapping for proper organization
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

# Read contact.html
with open('contact.html', 'r') as f:
    contact_content = f.read()

# Generate product options
product_options = ['                                <option value="">-- Select Product --</option>\n']

for category in category_order:
    if category in products_by_category:
        products = sorted(products_by_category[category])
        if products:
            product_options.append(f'                                <optgroup label="{category}">\n')
            for product in products:
                product_options.append(f'                                    <option value="{product}">{product}</option>\n')
            product_options.append('                                </optgroup>\n')

product_options.append('                                <option value="Other">Other Equipment</option>\n')
product_options.append('                                <option value="General">General Inquiry</option>\n')

new_select_content = ''.join(product_options)

# Replace select content
select_pattern = r'(<select id="product" name="product">)(.*?)(</select>)'
contact_content = re.sub(select_pattern, r'\1\n' + new_select_content + '                            \3', contact_content, flags=re.DOTALL)

# Write back
with open('contact.html', 'w') as f:
    f.write(contact_content)

print(f"✓ Fixed contact.html product list")
print(f"  Total products: {sum(len(p) for p in products_by_category.values())}")
for cat in category_order:
    if cat in products_by_category:
        print(f"  {cat}: {len(products_by_category[cat])} products")

