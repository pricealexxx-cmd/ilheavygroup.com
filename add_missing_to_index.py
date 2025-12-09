#!/usr/bin/env python3
"""
Add all missing products to index.html homepage
"""

import re
import subprocess
import os

def get_product_info(url):
    """Get product information from source page"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    # Title
    title_match = re.search(r'<title>([^<]+)', html)
    title = title_match.group(1).split('|')[0].strip() if title_match else ""
    title = title.replace('&#8212;', '-').replace('&amp;', '&').replace('&#8217;', "'")
    
    # Price
    price_match = re.search(r'\$([0-9,]+)', html)
    price = price_match.group(0) if price_match else "Contact for Price"
    
    # Year
    year = ""
    for pattern in [
        r'<li><span>Year:</span>\s*(\d{4})',
        r'Year[:\s]+(\d{4})',
    ]:
        match = re.search(pattern, html, re.I)
        if match:
            year = match.group(1)
            break
    
    # Hours
    hours = ""
    for pattern in [
        r'<li><span>(?:Hours|Usage):</span>\s*([0-9,]+)',
        r'(?:Hours|Usage)[:\s]+([0-9,]+)',
    ]:
        match = re.search(pattern, html, re.I)
        if match:
            hours = match.group(1).replace(',', '')
            break
    
    return {'title': title, 'price': price, 'year': year, 'hours': hours}

def categorize_product(title, url):
    """Determine product category"""
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
    
    return 'Compact Track Loaders'  # Default

def generate_product_card(product):
    """Generate HTML for product card"""
    slug = product['slug']
    title = product['title']
    price = product['price']
    year = product['year']
    hours = product['hours']
    
    # Check if main image exists
    main_img = f"images/{slug}/main.jpg"
    if not os.path.exists(main_img):
        main_img = f"https://via.placeholder.com/400x300?text={title[:20]}"
    
    # Short description
    desc = f"{title} - Premium equipment ready for work."
    if len(desc) > 80:
        desc = title[:60] + " - Premium equipment ready for work."
    
    card = f'''                    <div class="product-card">
                        <div class="product-image">
                            <img src="{main_img}" alt="{title}">
                            <div style="position: absolute; top: 10px; right: 10px; background: var(--primary-color); color: white; padding: 0.5rem 1rem; border-radius: 5px; font-weight: 600; font-size: 0.9rem;">Used</div>
                        </div>
                        <div class="product-content">
                            <h3>{title}</h3>
                            <p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;">{price}</p>
                            <p>{desc}</p>
                            <div class="product-specs">
                                <span><strong>Year:</strong> {year}</span>
                                <span><strong>Hours:</strong> {hours}</span>
                            </div>
                            <a href="product-{slug}.html" class="btn btn-secondary">Details</a>
                        </div>
                    </div>
'''
    return card

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# Get all products and categorize
products_by_category = {}
existing_slugs = set()

# Read index.html to find existing products
with open('index.html', 'r') as f:
    index_content = f.read()

# Find all existing product links
existing_links = re.findall(r'href="product-([^"]+\.html)"', index_content)
for link in existing_links:
    existing_slugs.add(link.replace('.html', ''))

print(f"Processing {len(urls)} products...\n")

for url in urls:
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    # Skip if already exists
    if clean_slug in existing_slugs:
        continue
    
    if not os.path.exists(f"images/{clean_slug}"):
        print(f"  ⚠ Skipping {clean_slug} - no images")
        continue
    
    try:
        info = get_product_info(url)
        category = categorize_product(info['title'], url)
        
        if category not in products_by_category:
            products_by_category[category] = []
        
        products_by_category[category].append({
            'slug': clean_slug,
            'url': url,
            **info
        })
        print(f"  ✓ {info['title'][:50]} -> {category}")
    except Exception as e:
        print(f"  ✗ Error processing {clean_slug}: {e}")

print(f"\n✓ Found {sum(len(v) for v in products_by_category.values())} missing products to add\n")

# Category mapping
category_mapping = {
    'Compact Track Loaders': 'Compact Track Loaders',
    'Compact (Mini) Excavators': 'Compact (Mini) Excavators',
    'Backhoes': 'Backhoes',
    'Row Crop Tractors': 'Row Crop Tractors',
    'Telehandlers': 'Telehandlers',
    'Dump Trucks': 'Dump Trucks',
    'Motor Graders': 'Motor Graders',
}

# Add products to index.html
for category, products in products_by_category.items():
    if not products:
        continue
    
    html_category = category_mapping.get(category, category)
    print(f"Adding {len(products)} products to {html_category}...")
    
    # Generate product cards
    product_cards = '\n'.join([generate_product_card(p) for p in products])
    
    # Check if category section exists
    if f'<h3 class="category-title">{html_category}</h3>' in index_content:
        # Find the category section and add products
        pattern = f'(<h3 class="category-title">{re.escape(html_category)}</h3>\\s*<div class="products-grid">)'
        match = re.search(pattern, index_content)
        if match:
            # Insert products after opening products-grid
            index_content = index_content.replace(
                match.group(1),
                match.group(1) + '\n' + product_cards
            )
            print(f"  ✓ Added to existing {html_category} section")
    else:
        # Create new category section
        new_section = f'''
            <!-- Category: {html_category} -->
            <div class="category-section" style="margin-top: 4rem;">
                <h3 class="category-title">{html_category}</h3>
                <div class="products-grid">
{product_cards}                </div>
            </div>
'''
        # Insert before closing products section
        index_content = index_content.replace(
            '    </section>',
            new_section + '\n    </section>',
            1
        )
        print(f"  ✓ Created new {html_category} section")

# Save updated index.html
with open('index.html', 'w') as f:
    f.write(index_content)

print(f"\n✓ All missing products added to index.html!")





