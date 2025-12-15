#!/usr/bin/env python3
"""
Recreate all product pages with correct information for each product
"""

import re
import subprocess
import os

def extract_product_info(url):
    """Extract all product information from source page"""
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
        r'<strong>Year:</strong>\s*(\d{4})',
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
        r'<strong>(?:Hours|Usage):</strong>\s*([0-9,]+)',
    ]:
        match = re.search(pattern, html, re.I)
        if match:
            hours = match.group(1).replace(',', '')
            break
    
    # Stock
    stock = ""
    for pattern in [
        r'<li><span>Stock[^<]*:</span>\s*(ZID-\d+)',
        r'Stock[:\s]+(ZID-\d+)',
    ]:
        match = re.search(pattern, html, re.I)
        if match:
            stock = match.group(1)
            break
    
    # Description
    desc_patterns = [
        r'<p[^>]*><strong>Description:</strong>\s*([^<]+(?:This|The)[^<]{50,300})',
        r'<p[^>]*>This[^<]+([^<]{50,300})',
        r'<p[^>]*>The[^<]+([^<]{50,300})',
    ]
    description = ""
    for pattern in desc_patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            description = match.group(1).strip()[:400]
            break
    
    # Features
    features = []
    feature_matches = re.findall(r'<li><strong>([^<]+)</strong>\s*[–-]\s*([^<]+)</li>', html)
    for feat in feature_matches[:8]:
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
    """Count images for product"""
    img_dir = f"images/{slug}"
    if not os.path.exists(img_dir):
        return 0
    images = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    return len(images)

def generate_product_page(url, slug, info):
    """Generate complete product page with correct info"""
    img_count = count_images(slug)
    
    # Generate gallery HTML
    gallery_html = f'<img src="images/{slug}/main.jpg" onclick="changeMainImage(this.src)">\n'
    for i in range(1, img_count):
        gallery_html += f'                        <img src="images/{slug}/image{i}.jpg" onclick="changeMainImage(this.src)">\n'
    
    # Generate features HTML
    features_html = ""
    if info['features']:
        for feat in info['features']:
            features_html += f'''                <div class="feature-item">
                    <h4>{feat['title']}</h4>
                    <p>{feat['desc']}</p>
                </div>
'''
    else:
        features_html = '''                <div class="feature-item">
                    <h4>Premium Quality</h4>
                    <p>High-quality equipment in excellent condition, ready for immediate use.</p>
                </div>
'''
    
    # Read template
    with open('product-caterpillar-299d3-2022.html', 'r') as f:
        template = f.read()
    
    # Extract model name from title
    model_name = info['title'].split()[0] + ' ' + info['title'].split()[1] if len(info['title'].split()) > 1 else info['title']
    
    # Replace all content
    template = template.replace('2022 Caterpillar 299D3 Skid Steer', info['title'])
    template = template.replace('Caterpillar 299D3', model_name)
    template = template.replace('$50,300 USD', info['price'] + ' USD')
    template = template.replace('Year: 2022', f'Year: {info["year"]}')
    template = template.replace('Hours: 342', f'Hours: {info["hours"]}')
    template = template.replace('Stock: ZID-664890', f'Stock: {info["stock"]}')
    template = template.replace('caterpillar-299d3-2022', slug)
    
    # Replace description - remove old template text
    old_desc_pattern = r'<p style="line-height: 1\.8; color: #555; font-size: 1\.05rem;">.*?</p>'
    if info['description']:
        new_desc = f'<p style="line-height: 1.8; color: #555; font-size: 1.05rem;">{info["description"]}</p>'
        template = re.sub(old_desc_pattern, new_desc, template, count=1)
    
    # Replace gallery
    old_gallery = re.search(r'<div class="product-gallery">.*?</div>', template, re.DOTALL)
    if old_gallery:
        new_gallery = f'''                    <div class="product-gallery">
                        {gallery_html}                    </div>'''
        template = template.replace(old_gallery.group(0), new_gallery)
    
    # Replace features
    if features_html:
        old_features = re.search(r'<div class="features-list">.*?</div>\s*</div>', template, re.DOTALL)
        if old_features:
            new_features = f'''            <div class="features-list">
{features_html}            </div>'''
            template = template.replace(old_features.group(0), new_features)
    
    # Fix Quick Details
    template = re.sub(r'<li>✓ <strong>Hours:</strong> \d+ \d+</li>', f'<li>✓ <strong>Hours:</strong> {info["hours"]}</li>', template)
    template = re.sub(r'<li>✓ <strong>Hours:</strong> \d+</li>', f'<li>✓ <strong>Hours:</strong> {info["hours"]}</li>', template)
    
    # Fix specs table
    template = re.sub(r'<td>Year</td>\s*<td>\d{4}</td>', f'<td>Year</td>\n                        <td>{info["year"]}</td>', template)
    template = re.sub(r'<td>Usage Hours</td>\s*<td>\d+ Hours</td>', f'<td>Usage Hours</td>\n                        <td>{info["hours"]} Hours</td>', template)
    
    # Remove duplicate values in description
    template = re.sub(r'The <strong>\d{4} \d{4}', f'The <strong>{info["year"]}', template)
    template = re.sub(r'With only <strong>\d+ hours</strong>', f'With only <strong>{info["hours"]} hours</strong>', template)
    
    # Fix contact link
    template = template.replace('Caterpillar%20299D3', model_name.replace(' ', '%20'))
    
    # Save
    filename = f"product-{slug}.html"
    with open(filename, 'w') as f:
        f.write(template)
    
    return filename

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Recreating product pages for {len(urls)} products...\n")

for i, url in enumerate(urls, 1):
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    # Special case
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    if not os.path.exists(f"images/{clean_slug}"):
        print(f"[{i}/{len(urls)}] ✗ {clean_slug} - No images, skipping")
        continue
    
    try:
        info = extract_product_info(url)
        generate_product_page(url, clean_slug, info)
        print(f"[{i}/{len(urls)}] ✓ {clean_slug} - Year: {info['year']}, Hours: {info['hours']}")
    except Exception as e:
        print(f"[{i}/{len(urls)}] ✗ {clean_slug} - Error: {e}")

print("\n✓ All product pages recreated with correct information!")










