#!/usr/bin/env python3
"""
Fix product categories on index.html - move products to correct categories
"""

import re
import subprocess
import os

def get_product_info(url):
    """Get product information"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    title_match = re.search(r'<title>([^<]+)', html)
    title = title_match.group(1).split('|')[0].strip() if title_match else ""
    title = title.replace('&#8212;', '-').replace('&amp;', '&').replace('&#8217;', "'")
    
    price_match = re.search(r'\$([0-9,]+)', html)
    price = price_match.group(0) if price_match else "Contact for Price"
    
    year = ""
    for pattern in [r'<li><span>Year:</span>\s*(\d{4})', r'Year[:\s]+(\d{4})']:
        match = re.search(pattern, html, re.I)
        if match:
            year = match.group(1)
            break
    
    hours = ""
    for pattern in [r'<li><span>(?:Hours|Usage):</span>\s*([0-9,]+)', r'(?:Hours|Usage)[:\s]+([0-9,]+)']:
        match = re.search(pattern, html, re.I)
        if match:
            hours = match.group(1).replace(',', '')
            break
    
    return {'title': title, 'price': price, 'year': year, 'hours': hours}

def categorize_product(title, url):
    """Correct categorization"""
    title_lower = title.lower()
    url_lower = url.lower()
    combined = title_lower + ' ' + url_lower
    
    if 'backhoe' in combined:
        return 'Backhoes'
    elif 'telehandler' in combined or 'tl1255' in combined or 'tl1055' in combined or 'jlg' in combined or 'jcb-510' in combined:
        return 'Telehandlers'
    elif 'dump truck' in combined or 'kenworth' in combined or 'peterbilt' in combined:
        return 'Dump Trucks'
    elif 'motor grader' in combined or '770gp' in combined:
        return 'Motor Graders'
    elif 'tractor' in combined:
        if '8245' in combined or '6175' in combined or 'row crop' in combined:
            return 'Row Crop Tractors'
        return 'Sub-Compact Tractors'
    elif 'excavator' in combined or 'u55' in combined or 'u50' in combined or 'u48' in combined or 'kx-040' in combined or '316fl' in combined or '312f' in combined or '313flgc' in combined or '320' in combined or '320gc' in combined:
        return 'Compact (Mini) Excavators'
    elif 'skid steer' in combined or 'track loader' in combined or 't870' in combined or 't86' in combined or 't770' in combined or 'svl' in combined or '259d' in combined or '299d' in combined or '331g' in combined:
        return 'Compact Track Loaders'
    
    return 'Compact Track Loaders'

# Product mapping - slug to correct category
product_categories = {}

with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    try:
        info = get_product_info(url)
        category = categorize_product(info['title'], url)
        product_categories[clean_slug] = category
    except:
        pass

# Read index.html
with open('index.html', 'r') as f:
    content = f.read()

# Find all product cards and their current categories
# Remove incorrectly placed products from Sub-Compact Tractors
products_to_move = {}

# Find products in Sub-Compact Tractors that should be elsewhere
sub_compact_section = re.search(r'(<h3 class="category-title">Sub-Compact Tractors</h3>.*?</div>\s*</div>)', content, re.DOTALL)
if sub_compact_section:
    section_content = sub_compact_section.group(1)
    
    # Find all product cards in this section
    product_cards = re.findall(r'(<div class="product-card">.*?</div>\s*</div>\s*</div>)', section_content, re.DOTALL)
    
    for card in product_cards:
        # Extract slug from href
        slug_match = re.search(r'href="product-([^"]+\.html)"', card)
        if slug_match:
            slug = slug_match.group(1).replace('.html', '')
            if slug in product_categories:
                correct_category = product_categories[slug]
                if correct_category != 'Sub-Compact Tractors':
                    products_to_move[slug] = {
                        'card': card,
                        'category': correct_category
                    }

print(f"Found {len(products_to_move)} products to move to correct categories\n")

# Remove products from Sub-Compact Tractors
for slug, data in products_to_move.items():
    content = content.replace(data['card'], '')

# Group products by correct category
products_by_category = {}
for slug, data in products_to_move.items():
    category = data['category']
    if category not in products_by_category:
        products_by_category[category] = []
    products_by_category[category].append(data['card'])

# Add products to correct category sections
for category, cards in products_by_category.items():
    print(f"Adding {len(cards)} products to {category}...")
    
    product_cards_html = '\n'.join(cards)
    
    # Check if category exists
    if f'<h3 class="category-title">{category}</h3>' in content:
        # Add to existing section
        pattern = f'(<h3 class="category-title">{re.escape(category)}</h3>\\s*<div class="products-grid">)'
        match = re.search(pattern, content)
        if match:
            content = content.replace(
                match.group(1),
                match.group(1) + '\n' + product_cards_html
            )
            print(f"  ✓ Added to existing {category} section")
    else:
        # Create new section
        new_section = f'''
            <!-- Category: {category} -->
            <div class="category-section" style="margin-top: 4rem;">
                <h3 class="category-title">{category}</h3>
                <div class="products-grid">
{product_cards_html}                </div>
            </div>
'''
        # Insert before closing products section
        content = content.replace(
            '    </section>',
            new_section + '\n    </section>',
            1
        )
        print(f"  ✓ Created new {category} section")

# Save
with open('index.html', 'w') as f:
    f.write(content)

print("\n✓ Categories fixed!")










