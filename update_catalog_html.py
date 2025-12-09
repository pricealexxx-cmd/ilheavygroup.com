#!/usr/bin/env python3
"""
Update catalog.html and index.html with all products
"""

import json
import re
import os

# Load categorized products
with open('products_categorized.txt', 'r') as f:
    products_by_category = json.load(f)

print("Updating catalog and index pages...\n")

# Category mapping for HTML
category_mapping = {
    'Compact Track Loaders': 'Compact Track Loaders',
    'Compact (Mini) Excavators': 'Compact (Mini) Excavators',
    'Backhoes': 'Backhoes',
    'Sub-Compact Tractors': 'Sub-Compact Tractors',
    'Row Crop Tractors': 'Row Crop Tractors',
    'Telehandlers': 'Telehandlers',
    'Dump Trucks': 'Dump Trucks',
    'Motor Graders': 'Motor Graders',
    'Portable Air Compressors': 'Portable Air Compressors',
    'Zero-Turn Mowers': 'Zero-Turn Mowers'
}

def generate_product_card(product, is_compact=False):
    """Generate HTML for product card"""
    slug = product['slug']
    title = product['title'][:60]  # Truncate long titles
    price = product['price']
    year = product['year']
    hours = product['hours']
    
    # Check if main image exists
    main_img = f"images/{slug}/main.jpg"
    if not os.path.exists(main_img):
        main_img = f"https://via.placeholder.com/400x300?text={title[:20]}"
    
    if is_compact:
        return f'''                    <div class="product-card-compact">
                        <div class="product-image-compact">
                            <img src="{main_img}" alt="{title}">
                            <div style="position: absolute; top: 10px; right: 10px; background: var(--primary-color); color: white; padding: 0.3rem 0.8rem; border-radius: 5px; font-weight: 600; font-size: 0.8rem;">Used</div>
                        </div>
                        <div class="product-content-compact">
                            <h3>{title}</h3>
                            <p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;">{price}</p>
                            <p>{title} - Premium equipment in excellent condition.</p>
                            <div class="specs-grid-compact">
                                <div class="spec-item-compact">
                                    <span class="spec-label-compact">Year:</span>
                                    <span class="spec-value-compact">{year if year else 'N/A'}</span>
                                </div>
                                <div class="spec-item-compact">
                                    <span class="spec-label-compact">Hours:</span>
                                    <span class="spec-value-compact">{hours if hours else 'N/A'}</span>
                                </div>
                            </div>
                            <a href="product-{slug}.html" class="btn btn-primary" style="width: 100%; text-align: center;">Details</a>
                        </div>
                    </div>
'''
    else:
        return f'''                    <div class="product-card">
                        <div class="product-image">
                            <img src="{main_img}" alt="{title}">
                            <div style="position: absolute; top: 10px; right: 10px; background: var(--primary-color); color: white; padding: 0.5rem 1rem; border-radius: 5px; font-weight: 600; font-size: 0.9rem;">Used</div>
                        </div>
                        <div class="product-content">
                            <h3>{title}</h3>
                            <p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;">{price}</p>
                            <p>{title} - Premium equipment ready for work.</p>
                            <div class="product-specs">
                                <span><strong>Year:</strong> {year if year else 'N/A'}</span>
                                <span><strong>Hours:</strong> {hours if hours else 'N/A'}</span>
                            </div>
                            <a href="product-{slug}.html" class="btn btn-secondary">Details</a>
                        </div>
                    </div>
'''

# Update catalog.html
print("Updating catalog.html...")
with open('catalog.html', 'r') as f:
    catalog_content = f.read()

# For each category, add products to catalog
for category, products in products_by_category.items():
    if not products:
        continue
    
    html_category = category_mapping.get(category, category)
    print(f"  Adding {len(products)} products to {html_category}...")
    
    # Generate product cards
    product_cards = '\n'.join([generate_product_card(p, is_compact=True) for p in products])
    
    # Find category section and add products
    pattern = f'(<!-- CATEGORY.*?{html_category}.*?</div>\\s*</div>\\s*</div>)'
    replacement = f'\\1\n{product_cards}'
    
    # Try to find and replace
    if html_category in catalog_content:
        # Find the category section
        cat_pattern = f'(<div class="category-section"[^>]*>.*?<h2>{html_category}</h2>.*?<div class="products-grid-compact">)'
        match = re.search(cat_pattern, catalog_content, re.DOTALL)
        if match:
            # Insert products after opening products-grid-compact
            catalog_content = catalog_content.replace(
                match.group(1),
                match.group(1) + '\n' + product_cards
            )

with open('catalog.html', 'w') as f:
    f.write(catalog_content)

print("✓ catalog.html updated\n")

# Update index.html  
print("Updating index.html...")
with open('index.html', 'r') as f:
    index_content = f.read()

# Add products to index (limit to 3-4 per category for homepage)
for category, products in products_by_category.items():
    if not products:
        continue
    
    html_category = category_mapping.get(category, category)
    print(f"  Adding {min(len(products), 4)} products to {html_category} on homepage...")
    
    # Limit products for homepage
    limited_products = products[:4]
    product_cards = '\n'.join([generate_product_card(p, is_compact=False) for p in limited_products])
    
    # Find category section
    cat_pattern = f'(<h3 class="category-title">{html_category}</h3>\\s*<div class="products-grid">)'
    match = re.search(cat_pattern, index_content, re.DOTALL)
    if match:
        index_content = index_content.replace(
            match.group(1),
            match.group(1) + '\n' + product_cards
        )

with open('index.html', 'w') as f:
    f.write(index_content)

print("✓ index.html updated\n")
print("✓ All done! Products added to catalog and homepage.")





