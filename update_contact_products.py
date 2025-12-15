#!/usr/bin/env python3
"""
Update contact.html with all products from index.html
"""

import re
from collections import defaultdict

# Read index.html to extract all products
with open('index.html', 'r') as f:
    content = f.read()

# Extract all product titles and categorize them
products_by_category = defaultdict(list)

# Pattern to match product cards with category titles
category_pattern = r'<!-- Category: ([^>]+) -->.*?<h3 class="category-title">([^<]+)</h3>.*?<div class="products-grid">(.*?)</div>\s*</div>\s*</div>'
matches = re.finditer(category_pattern, content, re.DOTALL)

for match in matches:
    category_comment = match.group(1).strip()
    category_title = match.group(2).strip()
    products_html = match.group(3)
    
    # Extract product titles from this category
    product_pattern = r'<h3>([^<]+)</h3>'
    products = re.findall(product_pattern, products_html)
    
    for product in products:
        products_by_category[category_title].append(product.strip())

# Also get products from old categories (Bobcat products)
old_categories = {
    'Compact Track Loaders': ['Bobcat T450', 'Bobcat T590', 'Bobcat T770'],
    'Portable Air Compressors': ['Bobcat PA450VP', 'Bobcat PA425V', 'Bobcat PA1170P', 'Bobcat PA825V'],
    'Sub-Compact Tractors': ['Bobcat CT1021', 'Bobcat CT1025'],
    'Compact (Mini) Excavators': ['Bobcat E20', 'Bobcat E35', 'Bobcat E48', 'Bobcat E60', 'Bobcat E88'],
    'Zero-Turn Mowers': ['Bobcat ZT2000', 'Bobcat ZT3000', 'Bobcat ZT3500', 'Bobcat ZT5000'],
}

# Merge old categories
for cat, prods in old_categories.items():
    if cat not in products_by_category:
        products_by_category[cat] = []
    for prod in prods:
        if prod not in products_by_category[cat]:
            products_by_category[cat].append(prod)

# Read contact.html
with open('contact.html', 'r') as f:
    contact_content = f.read()

# Generate new product select options
product_options = ['<option value="">-- Select Product --</option>\n']

for category in sorted(products_by_category.keys()):
    products = sorted(products_by_category[category])
    if products:
        product_options.append(f'                                <optgroup label="{category}">\n')
        for product in products:
            # Create a clean value for the option
            value = product.replace(' ', '%20')
            product_options.append(f'                                    <option value="{product}">{product}</option>\n')
        product_options.append('                                </optgroup>\n')

product_options.append('                                <option value="Other">Other Equipment</option>\n')
product_options.append('                                <option value="General">General Inquiry</option>\n')

new_select_content = ''.join(product_options)

# Replace the select options
select_pattern = r'(<select id="product" name="product">)(.*?)(</select>)'
contact_content = re.sub(select_pattern, r'\1\n' + new_select_content + '                            \3', contact_content, flags=re.DOTALL)

# Write updated contact.html
with open('contact.html', 'w') as f:
    f.write(contact_content)

print(f"✓ Updated contact.html with {sum(len(p) for p in products_by_category.values())} products")
print(f"  Categories: {', '.join(sorted(products_by_category.keys()))}")










