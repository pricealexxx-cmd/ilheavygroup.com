#!/usr/bin/env python3
"""
Create HTML product pages for all downloaded products
"""

import re
import subprocess
import os
from pathlib import Path

def get_product_details(url):
    """Extract detailed product information"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html_content = result.stdout
    
    # Extract price
    price_match = re.search(r'\$([0-9,]+)', html_content)
    price = price_match.group(0) if price_match else "Contact for Price"
    
    # Extract year
    year_match = re.search(r'Year[:\s]+(\d{4})', html_content, re.IGNORECASE)
    year = year_match.group(1) if year_match else ""
    
    # Extract hours
    hours_match = re.search(r'(?:Hours|Usage)[:\s]+(\d+)', html_content, re.IGNORECASE)
    hours = hours_match.group(1) if hours_match else ""
    
    # Extract stock
    stock_match = re.search(r'Stock[:\s]+(ZID-\d+)', html_content, re.IGNORECASE)
    stock = stock_match.group(1) if stock_match else ""
    
    # Extract title
    title_match = re.search(r'<title>([^<]+)', html_content)
    title = title_match.group(1).split('|')[0].strip() if title_match else ""
    title = title.replace('&#8212;', '-').replace('&amp;', '&')
    
    # Extract description
    desc_patterns = [
        r'<p[^>]*><strong>Description:</strong>\s*([^<]+)',
        r'<p[^>]*>This[^<]+([^<]{50,300})',
        r'<p[^>]*>The[^<]+([^<]{50,300})',
    ]
    description = ""
    for pattern in desc_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
        if match:
            description = match.group(1).strip()[:300]
            break
    
    # Extract features
    features = []
    feature_matches = re.findall(r'<li><strong>([^<]+)</strong>\s*[–-]\s*([^<]+)</li>', html_content)
    for feat in feature_matches[:6]:
        features.append({'title': feat[0], 'desc': feat[1]})
    
    return {
        'title': title,
        'price': price,
        'year': year,
        'hours': hours,
        'stock': stock,
        'description': description,
        'features': features
    }

def count_images(slug):
    """Count images in product directory"""
    img_dir = f"images/{slug}"
    if not os.path.exists(img_dir):
        return 0
    images = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    return len(images)

def generate_product_page(url, slug, details):
    """Generate HTML product page"""
    img_count = count_images(slug)
    
    # Generate gallery HTML
    gallery_html = '<img src="images/{}/main.jpg" onclick="changeMainImage(this.src)">\n'.format(slug)
    for i in range(1, img_count):
        gallery_html += '                        <img src="images/{}/image{}.jpg" onclick="changeMainImage(this.src)">\n'.format(slug, i)
    
    # Generate features HTML
    features_html = ""
    for feat in details['features']:
        features_html += f'''                <div class="feature-item">
                    <h4>{feat['title']}</h4>
                    <p>{feat['desc']}</p>
                </div>
'''
    
    # Read template
    with open('product-caterpillar-299d3-2022.html', 'r') as f:
        template = f.read()
    
    # Replace content
    template = template.replace('2022 Caterpillar 299D3 Skid Steer', details['title'])
    template = template.replace('$50,300 USD', details['price'] + ' USD')
    template = template.replace('Year: 2022', f'Year: {details["year"]}')
    template = template.replace('Hours: 342', f'Hours: {details["hours"]}')
    template = template.replace('Stock: ZID-664890', f'Stock: {details["stock"]}')
    template = template.replace('caterpillar-299d3-2022', slug)
    template = template.replace('Caterpillar 299D3', details['title'].split()[0] + ' ' + details['title'].split()[1] if len(details['title'].split()) > 1 else details['title'])
    
    # Replace gallery
    old_gallery = re.search(r'<div class="product-gallery">.*?</div>', template, re.DOTALL)
    if old_gallery:
        new_gallery = f'''                    <div class="product-gallery">
                        {gallery_html}                    </div>'''
        template = template.replace(old_gallery.group(0), new_gallery)
    
    # Replace description
    if details['description']:
        desc_pattern = r'<p style="line-height: 1\.8; color: #555; font-size: 1\.05rem;">.*?</p>'
        new_desc = f'<p style="line-height: 1.8; color: #555; font-size: 1.05rem;">{details["description"]}</p>'
        template = re.sub(desc_pattern, new_desc, template, count=1)
    
    # Replace features
    if features_html:
        old_features = re.search(r'<div class="features-list">.*?</div>\s*</div>', template, re.DOTALL)
        if old_features:
            new_features = f'''            <div class="features-list">
{features_html}            </div>'''
            template = template.replace(old_features.group(0), new_features)
    
    # Save file
    filename = f"product-{slug}.html"
    with open(filename, 'w') as f:
        f.write(template)
    
    print(f"  ✓ Created: {filename}")
    return filename

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Creating product pages for {len(urls)} products...\n")

for i, url in enumerate(urls, 1):
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    print(f"[{i}/{len(urls)}] {clean_slug}")
    
    # Check if images exist
    if not os.path.exists(f"images/{clean_slug}"):
        print(f"  ✗ Images not found, skipping")
        continue
    
    try:
        details = get_product_details(url)
        generate_product_page(url, clean_slug, details)
    except Exception as e:
        print(f"  ✗ Error: {e}")
        continue

print("\n✓ All product pages created!")

